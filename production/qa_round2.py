"""核验本轮新增生产文件；不扫描参考附件与历史交付。"""
from pathlib import Path
import re, json, hashlib, base64, io, collections
import xml.etree.ElementTree as ET
from PIL import Image
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ContentStream
from fontTools.ttLib import TTFont
import pymupdf
from production import ROOT, PALETTE, MM, remove_unused_fonts

TASKS=['task-02-onsite','task-04-card-final','task-05-wristbands','task-06-passes-lanyards','task-07-signage','task-08-rollups','task-09-profile']
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def cleanup_fonts():
    for task in TASKS:
        folder=ROOT/task
        if not folder.exists():continue
        for path in folder.rglob('*.pdf'):
            reader=PdfReader(path);writer=PdfWriter()
            for p in reader.pages:remove_unused_fonts(p,reader);writer.add_page(p)
            if reader.metadata:writer.add_metadata(dict(reader.metadata))
            temp=path.with_suffix('.clean.pdf');writer.write(temp);temp.replace(path)

def main():
    failures=[];pdfs=[];svgs=[];images=[];forbidden=[];fonts=collections.Counter();palettes=set()
    logo_expected={v:digest(ROOT/'_reference'/f'sinopop-logo-{v}.svg') if (ROOT/'_reference'/f'sinopop-logo-{v}.svg').exists() else digest(ROOT/'assets'/f'sinopop-logo-{v}.svg') for v in ('white','black')}
    logo_ok=all(digest(ROOT/'assets'/f'sinopop-logo-{v}.svg')==h for v,h in logo_expected.items())
    if not logo_ok:failures.append('source-logo-hash')
    required=['task-02-onsite/onsite-04-kit.png','task-05-wristbands/wristbands-mockup.png','task-04-card-final/staff.csv','task-05-wristbands/batch-wristbands.py','task-06-passes-lanyards/passes.csv','task-06-passes-lanyards/batch-passes.py','task-07-signage/sign-family-overview.png','task-09-profile/README.md']
    for name in required:
        if not (ROOT/name).exists():failures.append('required-file:'+name)
    font_weights={}
    expected_weights={'Archivo-Regular':400,'Archivo-Bold':700,'Archivo-ExtraBold':800,'NotoSansSC-Regular':400,'NotoSansSC-Medium':500,'NotoSansSC-Bold':700,'NotoSansSC-Heavy':900}
    for name,weight in expected_weights.items():
        f=TTFont(ROOT/'assets/fonts'/(name+'.ttf'));actual=f['OS/2'].usWeightClass;font_weights[name]=actual
        if actual!=weight or 'fvar' in f:failures.append('font-instance:'+name)
    # 分开写出禁用检测词，避免审计脚本自己将其带回成品包。
    banned='ALL'+' ACCESS';old_color='#1B'+'1E24'
    retired_surface='#'+''.join(f'{value:02X}' for value in (20,25,38))
    retired_label='墨'+'蓝'
    for task in TASKS:
        folder=ROOT/task
        if not folder.exists():failures.append('missing-folder:'+task);continue
        for p in sorted(folder.rglob('*')):
            if not p.is_file() or '__pycache__' in p.parts or '_raw' in p.parts:continue
            rel=p.relative_to(ROOT).as_posix()
            if p.suffix.lower() in ('.md','.py','.csv','.json','.svg'):
                s=p.read_text(encoding='utf-8-sig')
                if banned in s or old_color.lower() in s.lower() or retired_surface.lower() in s.lower() or retired_label in s:forbidden.append(rel)
            if p.suffix=='.svg':
                doc=ET.parse(p);nlogo=0;nfont=0;text_count=0;badglyph=[]
                styles=''.join(x.text or '' for x in doc.iter() if x.tag.endswith('style'))
                embedded_fonts={}
                for name,data in re.findall(r"font-family:'([^']+)';src:url\(data:font/woff2;base64,([^)]*)\)",styles):
                    ff=TTFont(io.BytesIO(base64.b64decode(data)));embedded_fonts.setdefault(name,set()).update(ff.getBestCmap());nfont+=1
                for node in doc.iter():
                    for key in ('fill','stroke'):
                        value=node.get(key,'')
                        if value.startswith('#'):
                            palettes.add(value.upper())
                            if value.upper() not in PALETTE:failures.append(rel+':color:'+value)
                        elif value and value!='none':failures.append(rel+':non-palette-color:'+value)
                    href=node.get('{http://www.w3.org/1999/xlink}href',node.get('href',''))
                    if href.startswith('data:image/svg+xml;base64,'):
                        h=hashlib.sha256(base64.b64decode(href.split(',',1)[1])).hexdigest()
                        if h not in logo_expected.values():failures.append(rel+':logo-hash')
                        nlogo+=1
                    if node.tag.endswith('text'):
                        text_count+=1;family=node.get('font-family','');chars=''.join(node.itertext())
                        if not family and chars.strip():failures.append(rel+':unassigned-font')
                        if family not in embedded_fonts and chars.strip():failures.append(rel+':unembedded-svg-font:'+family)
                        for char in chars:
                            if family in embedded_fonts and ord(char) not in embedded_fonts[family]:badglyph.append(char)
                if badglyph:failures.append(rel+':missing-glyph:'+''.join(sorted(set(badglyph))))
                svgs.append({'file':rel,'logo_instances':nlogo,'embedded_font_subsets':nfont,'text_runs':text_count})
            elif p.suffix=='.pdf':
                reader=PdfReader(p);doc=pymupdf.open(p);entry={'file':rel,'pages':len(reader.pages),'page_checks':[]};isprint=p.name.endswith('-print.pdf');technical='technical' in p.stem
                for i,page in enumerate(reader.pages):
                    trim=page.trimbox;bleed=page.bleedbox;media=page.mediabox
                    boxes=(media.left<=bleed.left<trim.left<trim.right<bleed.right<=media.right and media.bottom<=bleed.bottom<trim.bottom<trim.top<bleed.top<=media.top)
                    if not boxes:failures.append(f'{rel}:page-{i+1}:boxes')
                    bleed_mm=round((float(trim.left)-float(bleed.left))/MM,3)
                    fd=page['/Resources'].get('/Font',{});fd=fd.get_object() if hasattr(fd,'get_object') else fd
                    for name,obj in fd.items():
                        f=obj.get_object();base=str(f.get('/BaseFont'));desc=f.get('/FontDescriptor')
                        if not desc and f.get('/DescendantFonts'):desc=f['/DescendantFonts'][0].get_object().get('/FontDescriptor')
                        desc=desc.get_object() if desc else {}
                        if not any(k in desc for k in ('/FontFile','/FontFile2','/FontFile3')):failures.append(f'{rel}:page-{i+1}:unembedded-font:'+base)
                        fonts[base.split('+')[-1]]+=1
                    ops=ContentStream(page.get_contents(),reader).operations
                    badrgb=[op.decode() for args,op in ops if op in (b'rg',b'RG',b'g',b'G')]
                    for args,op in ops:
                        if op in (b'rg',b'RG') and all(abs(float(v)-target/255)<.00001 for v,target in zip(args,(20,25,38))):failures.append(f'{rel}:page-{i+1}:retired-surface-rgb')
                        if op in (b'k',b'K') and all(abs(float(v)-target)<.00001 for v,target in zip(args,(18/38,13/38,0,217/255))):failures.append(f'{rel}:page-{i+1}:retired-surface-cmyk')
                    if isprint and badrgb:failures.append(f'{rel}:page-{i+1}:non-cmyk-paint')
                    cspace=page['/Resources'].get('/ColorSpace',{});cspace=cspace.get_object() if hasattr(cspace,'get_object') else cspace
                    spot_names=[]
                    for key,val in cspace.items():
                        val=val.get_object()
                        if isinstance(val,list) and str(val[0])=='/Separation':spot_names.append(str(val[1]))
                    if any(n!='/SP-GREEN' for n in spot_names):failures.append(f'{rel}:other-spot')
                    for key,obj in page['/Resources'].get('/XObject',{}).items():
                        ob=obj.get_object()
                        if isprint and ob.get('/Subtype')=='/Image' and str(ob.get('/ColorSpace')) not in ('/DeviceCMYK','/DeviceGray'):failures.append(f'{rel}:non-cmyk-image')
                    spans=[span for block in doc[i].get_text('dict')['blocks'] if 'lines' in block for ln in block['lines'] for span in ln['spans'] if span['text'].strip()]
                    sizes=[s['size'] for s in spans];minimum=min(sizes) if sizes else None
                    if minimum is not None and minimum<6.99:failures.append(f'{rel}:page-{i+1}:font-below-7:{minimum}')
                    text=doc[i].get_text()
                    if banned in text:forbidden.append(rel)
                    # 抽样解码所有页面，发现损坏 PDF 或缺失字体。
                    preview_scale=min(.4,400/max(doc[i].rect.width,doc[i].rect.height))
                    doc[i].get_pixmap(matrix=pymupdf.Matrix(preview_scale,preview_scale),alpha=False)
                    entry['page_checks'].append({'page':i+1,'trim_mm':[round(float(trim.width)/MM,3),round(float(trim.height)/MM,3)],'bleed_mm':bleed_mm,'boxes_valid':bool(boxes),'min_font_pt':round(minimum,3) if minimum else None,'spots':spot_names,'embedded_fonts':len(fd),'rgb_operators':len(badrgb)})
                doc.close();pdfs.append(entry)
            elif p.suffix.lower()=='.png':
                with Image.open(p) as im:
                    im.load();images.append({'file':rel,'size':list(im.size),'format':im.format})
                    if im.format!='PNG':failures.append(rel+':wrong-file-format')
                    if '/mobile/' in rel and im.size!=(1080,1920):failures.append(rel+':mobile-size')
                    if p.name in ('onsite-04-kit.png','wristbands-mockup.png') and max(im.size)<2400:failures.append(rel+':image-long-edge')
    for f in forbidden:failures.append(f+':forbidden-content')
    result={'status':'PASS' if not failures else 'FAIL','scope':'本轮 task-02 指定替换图及 task-04 至 task-09 新增文件；参考附件和旧轮文件不随包','palette':sorted(palettes),'source_logo_hashes':logo_expected,'source_logo_hash_match':logo_ok,'static_font_weights':font_weights,'counts':{'pdf':len(pdfs),'svg':len(svgs),'png':len(images),'pdf_pages':sum(x['pages'] for x in pdfs)},'embedded_pdf_fonts':dict(fonts),'failures':failures,'pdfs':pdfs,'svgs':svgs,'images':images,'notes':['原标志内部原生纯黑/纯白不改色；SVG 嵌入字节与原件一致。','AI 照片和已有照片的自然像素、抗锯齿不适用纯色平面色值检查。','印刷文件不承诺 ICC 打样匹配；SP-GREEN 替代色仅用于屏幕显示。','无绿色印刷内容的页面不建立无效专色版。','工艺 PDF 没有文字的页面无需字体资源。']}
    (ROOT/'qa-summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'status':result['status'],'counts':result['counts'],'failures':failures[:40]},ensure_ascii=False,indent=2))

if __name__=='__main__':
    import sys
    if '--clean-fonts' in sys.argv:cleanup_fonts()
    main()
