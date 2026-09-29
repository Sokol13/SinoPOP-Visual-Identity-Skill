"""独立只读修订验收；仅把证据写入 qa/revision-validation.json。"""
from pathlib import Path
import base64, hashlib, io, json, re, xml.etree.ElementTree as ET
import pymupdf
from fontTools.ttLib import TTFont
from PIL import Image
from pypdf import PdfReader
from pypdf.generic import ContentStream

ROOT = Path(__file__).resolve().parent
QA = ROOT / 'qa'
PALETTE = {'#111318','#1B1E24','#F7F8F4','#73F64B','#B7BDC5','#5A616C','#3A3F48','#D8DBD3'}
NS = '{http://www.w3.org/2000/svg}'
report = {'status':'passed', 'errors':[], 'warnings':[], 'scope':{}, 'fonts':[], 'svg':[], 'pdf':[], 'png':[], 'spot_pdf':[]}

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p): return p.relative_to(ROOT).as_posix()
def fail(message): report['errors'].append(message)
def han(text): return any('\u3400' <= c <= '\u9fff' for c in text)

snapshot = json.loads((QA/'original-files.json').read_text(encoding='utf-8-sig'))
ORIGINAL = Path(snapshot['original'])
baseline = {v['path']:v['sha256'] for v in snapshot['files']}
protected = lambda p: (p.startswith(('task-03-profile/','_source/','assets/')) or '/_raw/' in p)
changed=[]; added=[]; missing=[]; original_changes=[]; protected_changes=[]
for name, sha in baseline.items():
    op=ORIGINAL/name; np=ROOT/name
    if not op.exists() or digest(op)!=sha: original_changes.append(name)
    if not np.exists(): missing.append(name)
    elif digest(np)!=sha:
        changed.append(name)
        if protected(name): protected_changes.append(name)
for p in ROOT.rglob('*'):
    if p.is_file() and rel(p) not in baseline and '__pycache__' not in p.parts:
        added.append(rel(p))
report['scope']={'original_folder_unchanged':not original_changes,'changed_existing':sorted(changed),'new_files':sorted(added),'missing_files':missing,'protected_changed':protected_changes,'protected_original_files':sum(protected(p) for p in baseline)}
if original_changes: fail('Original folder changed: '+str(original_changes))
if missing: fail('Original files absent from revision working tree: '+str(missing))
if protected_changes: fail('Protected files changed: '+str(protected_changes))

for label, weight in [('Regular',400),('Medium',500),('Bold',700),('Heavy',900)]:
    p=ROOT/'assets/fonts'/f'NotoSansSC-{label}.ttf'
    if not p.exists(): fail('Missing static font '+p.name); continue
    f=TTFont(p); actual=f['OS/2'].usWeightClass
    item={'file':rel(p),'weight':actual,'static':'fvar' not in f,'glyphs':f['maxp'].numGlyphs}
    report['fonts'].append(item)
    if actual!=weight or 'fvar' in f: fail('Invalid static font '+p.name)

logos={digest(ROOT/'assets'/f'sinopop-logo-{v}.svg') for v in ['white','black']}
report['original_logo_sha256']={v:digest(ROOT/'assets'/f'sinopop-logo-{v}.svg') for v in ['white','black']}
for p in sorted((ROOT/'task-01-cards').rglob('*.svg')):
    tree=ET.parse(p); text=p.read_text(encoding='utf-8'); used_fonts=set(); cn=[]; sizes=[]; colors=set(); logo_count=0
    embedded={}
    for name,b64 in re.findall(r"font-family:'([^']+)';src:url\(data:font/woff2;base64,([^)]*)\)",text):
        f=TTFont(io.BytesIO(base64.b64decode(b64))); embedded[name]={'cmap':f.getBestCmap(),'weight':f['OS/2'].usWeightClass,'glyphs':f['maxp'].numGlyphs,'static':'fvar' not in f}
    for e in tree.iter():
        for k in ['fill','stroke']:
            value=e.get(k,'')
            if value.startswith('#'): colors.add(value.upper())
        if e.tag==NS+'image':
            href=e.get('{http://www.w3.org/1999/xlink}href',e.get('href',''))
            if href.startswith('data:image/svg+xml;base64,'):
                logo_count+=1
                if hashlib.sha256(base64.b64decode(href.split(',',1)[1])).hexdigest() not in logos: fail(rel(p)+' changed embedded logo')
        if e.tag==NS+'text':
            value=''.join(e.itertext()); family=e.get('font-family',''); size=float(e.get('font-size',0)); sizes.append(size);used_fonts.add(family)
            if family not in embedded: fail(rel(p)+' text font not embedded: '+family)
            else:
                missing_glyphs=sorted(set(c for c in value if not c.isspace() and ord(c) not in embedded[family]['cmap']))
                if missing_glyphs: fail(rel(p)+' missing glyphs in '+family+': '+str(missing_glyphs))
            if han(value):
                cn.append({'text':value,'font':family,'size':size})
                if size>=16 and family!='NotoSansSC-Heavy': fail(rel(p)+' large Chinese title not Heavy: '+value)
                if size<=10 and family=='NotoSansSC-Heavy': fail(rel(p)+' small Chinese still Heavy: '+value)
                if '微信号' in value and size<=10 and family not in ['NotoSansSC-Regular','NotoSansSC-Medium']: fail(rel(p)+' WeChat small Chinese weight not matched: '+value)
    if colors-PALETTE: fail(rel(p)+' invalid artwork colors: '+str(colors-PALETTE))
    if sizes and min(sizes)<6.999: fail(rel(p)+' text below 7pt')
    report['svg'].append({'file':rel(p),'colors':sorted(colors),'logos_original':logo_count,'min_pt':min(sizes) if sizes else None,'used_fonts':sorted(used_fonts),'embedded_fonts':{k:{x:v for x,v in info.items() if x!='cmap'} for k,info in embedded.items()},'chinese':cn})

def texts(p): return [''.join(e.itertext()) for e in ET.parse(p).iter(NS+'text')]
ticket=ROOT/'task-01-cards/01-ticket/front.svg'
if any('sinopop' in s.lower() for s in texts(ticket)): fail('Ticket front retains duplicated sinoPOP text')
front=ROOT/'task-01-cards/04-backstage/front.svg';back=ROOT/'task-01-cards/04-backstage/back.svg'
if '主办方' not in ''.join(texts(front)) or 'PROMOTER' not in ''.join(texts(front)):fail('Backstage card lacks promoter label')
if any(s!='sinopop.us' for s in texts(back)):fail('Backstage card reverse contains extra text: '+str(texts(back)))
if any('ALL ACCESS' in s for s in texts(front)+texts(back)):fail('Backstage card retains ALL ACCESS')

for p in sorted((ROOT/'task-01-cards').rglob('*.pdf')):
    if '.raw.' in p.name: continue
    doc=pymupdf.open(p); used=set(); sizes=[]; embedded={}; trims=[]; render_pages=0
    for pg in doc:
        pix=pg.get_pixmap(matrix=pymupdf.Matrix(1,1),alpha=False); render_pages+=1
        trims.append([round(pg.trimbox.width,3),round(pg.trimbox.height,3)])
        for block in pg.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                for sp in line['spans']:
                    if sp['text'].strip(): used.add(sp['font']);sizes.append(sp['size'])
                    if '\ufffd' in sp['text']: fail(rel(p)+' replacement characters')
        for font in pg.get_fonts(full=True):
            xref=font[0];name=font[3].split('+')[-1]
            if xref:
                extracted=doc.extract_font(xref)
                embedded[name]=bool(extracted[3])
    for name in used:
        if not embedded.get(name,False): fail(rel(p)+' actual font not embedded: '+name)
    if sizes and min(sizes)<6.99: fail(rel(p)+' min text under 7 pt')
    report['pdf'].append({'file':rel(p),'rendered_pages':render_pages,'min_pt':round(min(sizes),3) if sizes else None,'used_fonts':sorted(used),'embedded':{k:embedded.get(k,False) for k in sorted(used)},'trim_pt':trims})
    if 'spot' in p.name.lower() or 'press' in p.name.lower() or 'cmyk' in p.name.lower():
        reader=PdfReader(p); spaces=[];ops=[];rgb=[];image_spaces=[]
        def resources(res):
            if not res:return
            for name, val in res.get('/ColorSpace',{}).items(): spaces.append(str(val.get_object()))
            for key,val in res.get('/XObject',{}).items():
                obj=val.get_object()
                if obj.get('/Subtype')=='/Form':
                    scan_content(obj)
                    resources(obj.get('/Resources'))
                elif obj.get('/Subtype')=='/Image': image_spaces.append(str(obj.get('/ColorSpace')))
        def scan_content(stream):
            content=ContentStream(stream,reader)
            for operands, op in content.operations:
                ops.append(op.decode('ascii'))
                if op in [b'rg',b'RG']:rgb.append(list(operands))
        for pg in reader.pages:
            scan_content(pg.get_contents()); resources(pg.get('/Resources'))
        separation=any('/Separation' in s and '/SP-GREEN' in s for s in spaces)
        spot_used='scn' in ops or 'SCN' in ops
        if not separation or not spot_used:fail(rel(p)+' no actual SP-GREEN Separation ink')
        if rgb or any('RGB' in x for x in image_spaces):fail(rel(p)+' contains RGB paint or image color space')
        report['spot_pdf'].append({'file':rel(p),'SP-GREEN_Separation':separation,'spot_paint_operator':spot_used,'process_cmyk_operator':'k' in ops or 'K' in ops,'rgb_paint_count':len(rgb),'color_spaces':spaces,'image_color_spaces':image_spaces})

for p in sorted((ROOT/'task-02-onsite').glob('onsite-*.png')):
    with Image.open(p) as im: im.load();dims=im.size;fmt=im.format
    if max(dims)<2400 or fmt!='PNG':fail(rel(p)+' wrong dimensions or format')
    if rel(p) not in changed:fail(rel(p)+' not recomposed')
    report['png'].append({'file':rel(p),'size':dims,'format':fmt,'decode':'passed'})

report['status']='passed' if not report['errors'] else 'failed'
(QA/'revision-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':report['status'],'errors':report['errors'],'counts':{k:len(report[k]) for k in ['svg','pdf','png','spot_pdf']},'changed_existing_count':len(changed),'new_files_count':len(added),'protected_changed':protected_changes},ensure_ascii=False,indent=2))
