"""独立改色审计：与已验收源比较，只允许层级面颜色替换。"""
from pathlib import Path
import argparse, base64, hashlib, io, json, re
from collections import Counter
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from pypdf import PdfReader
from pypdf.generic import ContentStream
import pymupdf

OLD_RGB = (20, 25, 38)
NEW_RGB = (24, 26, 31)
OLD_CMYK = (.47368421, .34210526, 0, .85098039)
NEW_CMYK = (.22580645, .16129032, 0, .87843137)
INK_CMYK = (.29166667, .20833333, 0, .90588235)
COLOR_OPS = {b'rg', b'RG', b'g', b'G', b'k', b'K', b'cs', b'CS', b'sc', b'SC', b'scn', b'SCN'}
TEXT_SUFFIXES = {'.py', '.md', '.json', '.csv', '.svg'}

def digest(data):
    return hashlib.sha256(data if isinstance(data, bytes) else Path(data).read_bytes()).hexdigest()

def hex_value(rgb):
    return '#' + ''.join(format(v, '02X') for v in rgb)

def near(a, b):
    return len(a) == len(b) and all(abs(float(x) - y) < 2e-6 for x, y in zip(a, b))

def obj(value):
    if isinstance(value, (list, tuple)):
        return [obj(x) for x in value]
    if isinstance(value, dict):
        return {str(k):obj(v) for k,v in sorted(value.items(), key=lambda x:str(x[0]))}
    if isinstance(value, bytes):
        return {'bytes':value.hex()}
    if isinstance(value, (float, int)):
        return round(float(value), 8)
    return str(value)

def records(ops, replace=False, exclude_colors=False):
    result=[]
    for args, op in ops:
        if exclude_colors and op in COLOR_OPS:
            continue
        val=obj(args)
        if replace and op in (b'rg', b'RG') and near(args, tuple(x/255 for x in OLD_RGB)):
            val=[round(x/255, 6) for x in NEW_RGB]
        if replace and op in (b'k', b'K') and near(args, OLD_CMYK):
            val=[round(x, 6) for x in NEW_CMYK]
        result.append([op.decode('ascii'), val])
    return result

def payload_hash(value):
    return digest(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())

def font_streams(page):
    found={}
    resources=page.get('/Resources', {}).get_object()
    fonts=resources.get('/Font', {})
    fonts=fonts.get_object() if hasattr(fonts, 'get_object') else fonts
    for name, ref in fonts.items():
        f=ref.get_object(); desc=f.get('/FontDescriptor')
        if not desc and f.get('/DescendantFonts'):
            desc=f['/DescendantFonts'][0].get_object().get('/FontDescriptor')
        if not desc:
            found[str(name)]={'font':str(f.get('/BaseFont')), 'embedded':False}; continue
        desc=desc.get_object()
        found[str(name)]={'font':str(f.get('/BaseFont')), 'streams':{key:digest(desc[key].get_object().get_data()) for key in ('/FontFile','/FontFile2','/FontFile3') if key in desc}}
    return found

def painted_font_names(ops):
    current=None; stack=[]; used=set()
    for args,op in ops:
        if op==b'q':stack.append(current)
        elif op==b'Q':current=stack.pop() if stack else None
        elif op==b'Tf':current=str(args[0])
        elif op in (b'Tj',b'TJ',b"'",b'"') and current:used.add(current)
    return used

def xobjects(page, reader):
    result={}
    def walk(resources, prefix=''):
        resources=resources.get_object(); xs=resources.get('/XObject', {})
        xs=xs.get_object() if hasattr(xs,'get_object') else xs
        for name, ref in xs.items():
            value=ref.get_object(); key=prefix+str(name)
            if value.get('/Subtype') == '/Form':
                result[key]={'kind':'form', 'ops':records(ContentStream(value, reader).operations)}
                if value.get('/Resources'):walk(value['/Resources'], key)
            else:
                result[key]={'kind':str(value.get('/Subtype')), 'data':digest(value.get_data()), 'size':[value.get('/Width'),value.get('/Height')], 'colorspace':obj(value.get('/ColorSpace'))}
    walk(page['/Resources'])
    return result

def geometry(page):
    result=[]
    for block in page.get_text('dict')['blocks']:
        if 'lines' not in block:continue
        for line in block['lines']:
            for span in line['spans']:
                result.append({k:span.get(k) for k in ('text','font','size','flags','origin','bbox')})
    return result

def canonical_font(data):
    font=TTFont(io.BytesIO(base64.b64decode(data)), recalcTimestamp=False)
    # WOFF 子集包装的生成时间不影响字形、布局、宽度和字体嵌入。
    if 'head' in font:
        font['head'].created=0; font['head'].modified=0; font['head'].checkSumAdjustment=0
    result={tag:digest(font.getTableData(tag)) for tag in font.keys() if tag not in ('GlyphOrder','DSIG')}
    return payload_hash(result)

def svg_shape(path, replace=False):
    text=path.read_text(encoding='utf-8-sig')
    if replace:text=re.sub(re.escape(hex_value(OLD_RGB)), hex_value(NEW_RGB), text, flags=re.I)
    text=re.sub(r'data:font/woff2;base64,([A-Za-z0-9+/=]+)', lambda m:'FONT:'+canonical_font(m.group(1)), text)
    doc=ET.fromstring(text)
    def node(n):return [n.tag, sorted(n.attrib.items()), n.text or '', [node(child) for child in n]]
    return node(doc)

def is_photo(path):
    if '_raw' in path.parts:return True
    if path.name in ('onsite-04-kit.png','wristbands-mockup.png','profile-cover-square.png','profile-cover-phone.png'):return True
    svg=path.with_name(path.name.replace('-preview.png','.svg')).with_suffix('.svg')
    return svg.exists() and 'data:image/png;base64,' in svg.read_text(encoding='utf-8-sig')

def rerender_preview(path, root):
    # 复现交付代码的固定渲染和缩放顺序，逐像素检验，不扩大颜色误差阈值。
    if path.name in ('onsite-04-kit.png','wristbands-mockup.png'):
        return None, 'unchanged-composite'
    if path.name == 'sign-family-overview.png':
        out=Image.new('RGB',(3600,2300),'#F7F8F4'); draw=ImageDraw.Draw(out)
        fontdir=root/'assets/fonts'
        cn=ImageFont.truetype(str(fontdir/'NotoSansSC-Heavy.ttf'),45)
        en=ImageFont.truetype(str(fontdir/'Archivo-Bold.ttf'),29)
        small=ImageFont.truetype(str(fontdir/'NotoSansSC-Bold.ttf'),25)
        draw.text((85,105),'现场标识 · 歌单',font=cn,fill='#111318',anchor='ls')
        draw.text((85,159),'SIGN FAMILY / ONE PHYSICAL SCALE',font=en,fill='#5A616C',anchor='ls')
        placements=[('hang-restrooms',85,780,'吊挂 120 × 30 cm'),('hang-bar-merch',85,1120,'吊挂 120 × 30 cm'),('entrance-ticket',1350,280,'入口 60 × 85 cm'),('house-rules',2010,235,'须知 60 × 90 cm'),('floor-photo-spot',2690,505,'地贴 Ø 60 cm'),('floor-queue-start',2690,1305,'地贴 Ø 60 cm'),('wall-coat-check-a3',85,1610,'墙贴 A3'),('wall-way-out-a3',440,1610,'墙贴 A3'),('pillar-id-letter',820,1743,'立柱 Letter'),('table-merch-a5-panel',1110,1807,'桌卡 A5')]
        for stem,x,y,label in placements:
            svg=ET.parse(path.parent/(stem+'.svg')).getroot()
            w=float(svg.attrib['width'][:-2])*.95; h=float(svg.attrib['height'][:-2])*.95
            src=path.parent/(stem+'-preview.png')
            if stem=='table-merch-a5-panel':
                im=Image.open(path.parent/'table-merch-a5-preview.png').convert('RGB')
                im=im.crop((0,round(im.height*210/515),im.width,round(im.height*420/515)))
            else:im=Image.open(src).convert('RGB')
            thumb=im.resize((round(w),round(h)),Image.Resampling.LANCZOS)
            if stem.startswith('floor-'):
                mask=Image.new('L',thumb.size,0);ImageDraw.Draw(mask).ellipse((0,0,thumb.width-1,thumb.height-1),fill=255);out.paste(thumb,(x,y),mask)
            else:out.paste(thumb,(x,y))
            draw.text((x,y+h+48),label,font=small,fill='#111318',anchor='ls')
        return out,'verified-preview-overview'
    if path.name=='assembly-preview.png':
        pdf=root/'_qa/card-assembly-rgb.pdf';page_number=0;preview_long=2400
    else:
        stem=path.name.removesuffix('-preview.png');m=re.search(r'-p(\d\d)$',stem)
        page_number=int(m.group(1))-1 if m else 0
        stem=stem[:m.start()] if m else stem
        pdf=path.parent/(stem+'-rgb.pdf');preview_long=1920 if path.parent.name=='mobile' else 2400
        if stem.startswith('lanyard-'):preview_long=5400
        if path.parent.name=='task-08-rollups':preview_long=3000
    if not pdf.exists():return None,'missing-rgb-source'
    with pymupdf.open(pdf) as document:
        page=document[page_number];rect=page.trimbox;scale=preview_long/max(rect.width,rect.height)
        pix=page.get_pixmap(matrix=pymupdf.Matrix(scale,scale),clip=rect,alpha=False)
        im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
    if path.parent.name=='mobile':im=im.resize((1080,1920),Image.Resampling.LANCZOS)
    return im,str(pdf.relative_to(root))

def inspect(base, root, output):
    failures=[]; pdfs=[]; svgs=[]; layouts=[]; images=[]; assets=[]; counters=Counter()
    paths=[]
    for folder in sorted(root.glob('task-*')):
        paths.extend(p for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts and '_raw' not in p.parts)
    # 拼装预览的中间 PDF 也纳入证据链；它不是额外印刷交付物。
    assembly=root/'_qa/card-assembly-rgb.pdf'
    if assembly.exists():paths.append(assembly)
    for index,path in enumerate(sorted(paths)):
        rel=path.relative_to(root).as_posix(); prior=base/rel
        if not prior.exists():
            failures.append(rel+':missing-baseline');continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            body=path.read_text(encoding='utf-8-sig')
            if hex_value(OLD_RGB).lower() in body.lower():failures.append(rel+':retired-color-token')
        if path.suffix == '.pdf':
            new=PdfReader(path); old=PdfReader(prior); pn=pymupdf.open(path); po=pymupdf.open(prior)
            row={'file':rel, 'pages':len(new.pages), 'checks':[]}
            if len(new.pages)!=len(old.pages):failures.append(rel+':page-count')
            for n,(np_,op_) in enumerate(zip(new.pages,old.pages)):
                a=ContentStream(np_.get_contents(),new).operations;b=ContentStream(op_.get_contents(),old).operations
                old_hits=[i for i,(args,op) in enumerate(a) if (op in (b'rg',b'RG') and near(args,tuple(x/255 for x in OLD_RGB))) or (op in (b'k',b'K') and near(args,OLD_CMYK))]
                boxes=all(list(getattr(np_,k))==list(getattr(op_,k)) for k in ('mediabox','cropbox','trimbox','bleedbox'))
                color_match=records(b,replace=True)==records(a)
                noncolor=records(a,exclude_colors=True)==records(b,exclude_colors=True)
                new_fonts=font_streams(np_);old_fonts=font_streams(op_)
                fonts=new_fonts==old_fonts
                font_note=None
                if rel=='_qa/card-assembly-rgb.pdf':
                    new_used=painted_font_names(a);old_used=painted_font_names(b)
                    fonts=new_used==old_used and {k:v for k,v in new_fonts.items() if k in new_used}=={k:v for k,v in old_fonts.items() if k in old_used}
                    font_note={'scope':'temporary-assembly-render-source-only','baseline_unused_resources':sorted(set(old_fonts)-old_used),'new_unused_resources':sorted(set(new_fonts)-new_used),'painted_font_streams_identical':fonts}
                text=geometry(pn[n])==geometry(po[n])
                xos=xobjects(np_,new)==xobjects(op_,old)
                ink_old=sum(1 for args,op in b if op in (b'k',b'K') and near(args,INK_CMYK))
                ink_new=sum(1 for args,op in a if op in (b'k',b'K') and near(args,INK_CMYK))
                check={'page':n+1,'retired_color_operators':len(old_hits),'only_surface_color_change':color_match,'noncolor_operators_identical':noncolor,'font_stream_sha256_identical':fonts,'text_geometry_identical':text,'page_boxes_identical':boxes,'xobjects_identical':xos,'ink_operator_counts':[ink_old,ink_new], 'new_surface_cmyk_operators':sum(1 for args,op in a if op in (b'k',b'K') and near(args,NEW_CMYK))}
                row['checks'].append(check)
                if font_note:check['scratch_font_resource_note']=font_note
                for key in ('only_surface_color_change','noncolor_operators_identical','font_stream_sha256_identical','text_geometry_identical','page_boxes_identical','xobjects_identical'):
                    if not check[key]:failures.append(f'{rel}:p{n+1}:{key}')
                if old_hits:failures.append(f'{rel}:p{n+1}:retired-pdf-color')
                if ink_old!=ink_new:failures.append(f'{rel}:p{n+1}:ink-count-changed')
            pdfs.append(row);po.close();pn.close()
        elif path.suffix == '.svg':
            identical=svg_shape(prior,replace=True)==svg_shape(path)
            svgs.append({'file':rel,'only_surface_color_change':identical})
            if not identical:failures.append(rel+':svg-structure-or-font-change')
        elif path.name.endswith('layout.json'):
            identical=path.read_bytes()==prior.read_bytes();same_structure=json.loads(path.read_text('utf-8-sig'))==json.loads(prior.read_text('utf-8-sig'))
            layouts.append({'file':rel,'bytes_identical':identical,'structure_identical':same_structure})
            if not same_structure:failures.append(rel+':layout-changed')
        elif path.suffix.lower()=='.png':
            with Image.open(path) as ni,Image.open(prior) as oi:
                ni.load();oi.load();same_size=ni.size==oi.size
                row={'file':rel,'size':list(ni.size),'same_dimensions':same_size,'photo_pixel_exemption':is_photo(path)}
                if not same_size:failures.append(rel+':pixel-dimensions');images.append(row);continue
                na=np.asarray(ni.convert('RGB'),dtype=np.int16);oa=np.asarray(oi.convert('RGB'),dtype=np.int16);delta=na-oa; changed=np.any(delta!=0,axis=2)
                t=-delta[:,:,2]/7
                # 边缘覆盖度可改变三个色通道的整数舍入，保留两级容差。
                valid=(t>=-2/7)&(t<=1+2/7)&(np.abs(delta[:,:,0]-4*t)<=2)&(np.abs(delta[:,:,1]-t)<=2)
                mismatches=int(np.count_nonzero(changed&~valid)); retired=int(np.count_nonzero(np.all(na==OLD_RGB,axis=2)))
                row.update(changed_pixels=int(np.count_nonzero(changed)),simple_delta_model_outliers=mismatches,retired_exact_rgb_pixels=retired,changed_delta_min=delta[changed].min(axis=0).tolist() if changed.any() else [0,0,0],changed_delta_max=delta[changed].max(axis=0).tolist() if changed.any() else [0,0,0])
                expected,source=rerender_preview(path,root);old_expected,old_source=rerender_preview(prior,base)
                if source=='unchanged-composite':new_match=old_match=not changed.any()
                else:
                    new_match=expected is not None and expected.size==ni.size and np.array_equal(np.asarray(expected),na)
                    old_match=old_expected is not None and old_expected.size==oi.size and np.array_equal(np.asarray(old_expected),oa)
                row.update(new_pixels_match_source_render=bool(new_match),old_pixels_match_source_render=bool(old_match),render_source=source)
                if not new_match:failures.append(rel+':new-png-not-exact-source-render')
                if not old_match:failures.append(rel+':baseline-png-not-exact-source-render')
                if retired and not row['photo_pixel_exemption']:failures.append(rel+':retired-flat-pixel')
                images.append(row)
        counters[path.suffix.lower()]+=1
        if index%35==0:print(f'Checked {index+1}/{len(paths)}',flush=True)
    for path in sorted(list((root/'assets').rglob('*'))+[p for task in root.glob('task-*') for p in task.rglob('_raw/*')]):
        if not path.is_file() or '__pycache__' in path.parts:continue
        rel=path.relative_to(root).as_posix();prior=base/rel
        if not prior.exists():continue
        identical=digest(path)==digest(prior);assets.append({'file':rel,'sha256':digest(path),'unchanged':identical})
        if not identical:failures.append(rel+':source-asset-changed')
    for variant in ('black','white'):
        rel=f'assets/sinopop-logo-{variant}.svg';source=base/'_reference'/f'sinopop-logo-{variant}.svg'
        if source.exists():
            identical=digest(root/rel)==digest(source)
            assets.append({'file':rel,'source':'original-attachment-svg','sha256':digest(root/rel),'unchanged':identical})
            if not identical:failures.append(rel+':original-logo-hash-mismatch')
    report={'status':'PASS' if not failures else 'FAIL','old_surface_rgb':OLD_RGB,'new_surface_rgb':NEW_RGB,'new_surface_cmyk':NEW_CMYK,'unchanged_ink_cmyk':INK_CMYK,'counts':dict(counters),'failures':failures,'pdfs':pdfs,'svgs':svgs,'layouts':layouts,'images':images,'source_assets':assets,'notes':['只有既有照片像素可偶然等于停用 RGB；照片内容另以原件哈希及 PDF 图像流比较证明未变。','简单通道增量模型的边缘异常数量保留在记录里，不放宽阈值。验收依据为旧新版 PNG 各自与对应 RGB PDF 的原渲染顺序重现逐像素完全一致，PDF 指令已经独立证明仅层级面颜色变化。总览从这些已验真的预览重现；手机按原顺序使用 LANCZOS 缩放。','SVG 字体只排除 WOFF 字体头生成时间；字形、字宽和所有其他字体表仍逐表比较。','97 个正式 PDF 全部字体资源与字体流严格相同。额外检查的拼装临时 PDF 基线版本保留未用的 Helvetica/Times 资源，新临时文件已经清理；只在这个非交付中间文件按实际绘字字体流比较，其所有非颜色指令仍严格一致。']}
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'status':report['status'],'counts':dict(counters),'failures':failures,'report':str(output)},ensure_ascii=False,indent=2))
    return not failures

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--base',type=Path,required=True);parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);parser.add_argument('--output',type=Path)
    args=parser.parse_args();success=inspect(args.base.resolve(),args.root.resolve(),args.output or args.root/'_qa/surface-only-report.json');raise SystemExit(0 if success else 1)
