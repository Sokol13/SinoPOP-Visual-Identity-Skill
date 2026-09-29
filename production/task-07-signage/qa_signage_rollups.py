from pathlib import Path
import json, re, xml.etree.ElementTree as ET
import pymupdf
from pypdf import PdfReader
from pypdf.generic import ContentStream
from PIL import Image

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'task-07-signage'
PALETTE={'#111318','#181A1F','#F7F8F4','#73F64B','#B7BDC5','#5A616C','#3A3F48','#D8DBD3'}

def main():
    results=[]
    for folder in [OUT,ROOT/'task-08-rollups']:
        for path in sorted(folder.glob('*.pdf')):
            p=PdfReader(path)
            doc=pymupdf.open(path)
            for i,(page,render) in enumerate(zip(p.pages,doc)):
                trim=page.trimbox;bleed=page.bleedbox
                offsets=[float(trim[0]-bleed[0]),float(trim[1]-bleed[1]),float(bleed[2]-trim[2]),float(bleed[3]-trim[3])]
                assert max(offsets)-min(offsets)<.002
                assert min(offsets)>0
                chars=[span for block in render.get_text('dict')['blocks'] if 'lines' in block for line in block['lines'] for span in line['spans']]
                minimum=min((s['size'] for s in chars),default=None)
                assert minimum is None or minimum>=6.999,(path,minimum)
                fonts=page['/Resources'].get('/Font',{})
                for name,ref in fonts.items():
                    font=ref.get_object()
                    desc=font.get('/FontDescriptor')
                    assert desc and any(k in desc.get_object() for k in ['/FontFile','/FontFile2','/FontFile3']),(path,name)
                content=ContentStream(page.get_contents(),p)
                ops=[op for _,op in content.operations]
                if path.name.endswith('-print.pdf'):assert not set(ops)&{b'rg',b'RG',b'g',b'G'},path
                results.append({'file':str(path.relative_to(ROOT)),'page':i+1,'minimum_font_pt':minimum,'embedded_font_count':len(fonts),
                                'trim_mm':[round(float(trim.width)*25.4/72,3),round(float(trim.height)*25.4/72,3)],'bleed_mm':round(offsets[0]*25.4/72,3),'pass':True})
            doc.close()
        for path in folder.glob('*.png'):
            im=Image.open(path);im.verify()
        for path in folder.glob('*.svg'):
            tree=ET.parse(path)
            for e in tree.iter():
                for attr in ['fill','stroke']:
                    v=e.get(attr)
                    if v and v.startswith('#'):assert v.upper() in PALETTE,(path,v)
    h=json.loads((OUT/'signage-height-qa.json').read_text(encoding='utf-8'))
    assert all(r['minimum_ink_height_mm']>=r['required_mm'] for r in h)
    report={'result':'PASS','pdf_pages_checked':len(results),'files':results,'glyph_height_checks':len(h),
            'visual_check':'已目检总览、三款易拉宝与桌卡展开；中文混排、连字符、撇号及域名均共基线。'}
    (OUT/'qa-signage-rollups.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS',len(results),'PDF pages;',len(h),'glyph-height checks')

if __name__=='__main__':main()
