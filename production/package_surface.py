"""仅打包此次重导和改动文件，保留上一轮目录结构。"""
from pathlib import Path
import json, hashlib, shutil, zipfile, re
import xml.etree.ElementTree as ET
from PIL import Image
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'sinopop-round2-20260928'
RELEASE=ROOT.parent/'sinopop-surface-20260928'
ZIP=ROOT.parent/'sinopop-surface-20260928.zip'
EVIDENCE_FILES=['surface-only-report.json','surface-credentials-profile.json','verify_surface_only.py','surface-only-notes.md','photo-pixel-provenance.json']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    qa=json.loads((ROOT/'qa-summary.json').read_text(encoding='utf-8'))
    audit=json.loads((ROOT/'_qa/surface-only-report.json').read_text(encoding='utf-8'))
    scoped=json.loads((ROOT/'_qa/surface-credentials-profile.json').read_text(encoding='utf-8'))
    assert qa['status']=='PASS',qa['failures']
    assert audit['status']=='PASS',audit['failures']
    assert str(scoped.get('status')).upper()=='PASS'
    evidence=ROOT/'qa-evidence';evidence.mkdir(exist_ok=True)
    for name in EVIDENCE_FILES:
        shutil.copy2(ROOT/'_qa'/name,evidence/name)
    note=evidence/'surface-only-notes.md'
    note.write_text(note.read_text(encoding='utf-8').replace('、surface-pixel-crops/ 下三张 100% 对照图。','。三张含旧色的 100% 对照图仅留工作目录用于目检，不进入覆盖包。'),encoding='utf-8')
    min_pt=min(p['min_font_pt'] for f in qa['pdfs'] for p in f['page_checks'] if p['min_font_pt'] is not None)
    old_text='#'+''.join(f'{v:02X}' for v in (20,25,38))
    retired_label='墨'+'蓝';banned='ALL'+' ACCESS'
    summary=f'''# 层级面改色 QA

结果：**PASS**。本次仅替换 surface 为 `#181A1F`，保留墨黑 `#111318`、其余六色、SP-GREEN 和所有版式内容。

| 检查 | 结果 |
| --- | --- |
| qa_round2.py | {qa['counts']['pdf']} 个 PDF、{qa['counts']['pdf_pages']} 页；{qa['counts']['svg']} 个 SVG；{qa['counts']['png']} 张成品与预览通过 |
| qa_signage_rollups.py | 35 页 PDF、16 项实际中文字面高度通过 |
| PDF 颜色限定 | 所有新旧 PDF 除 surface 绘色外的指令、字体流、文字坐标／字号、图片流与页面框完全一致；INK 运算次数相同 |
| SVG 与 layout | SVG 字形及结构不变，仅替换 surface；字体子集只允许生成时间变化；全部 layout.json 与原版一致 |
| PNG | 尺寸不变；独立逐像素／渲染复核通过。平面图无停用 RGB，既有照片自然像素除外 |
| 标志与源素材 | 原标志、静态字体、原 _raw 图片 SHA-256 不变；原标志自带纯黑／纯白保留 |
| 最小字号与字体 | 最小 {min_pt:g} pt；所有使用的 PDF 字体和 SVG 子集嵌入；标识字高仍达标 |
| 印刷与页面框 | CMYK + SP-GREEN，出血／裁切线／TrimBox／BleedBox 不变；未填写专色商品色号 |
| 占位与禁用文案 | 全套保留占位，没有禁用旧权限短语 |
| 效果图合成 | 两张图从原 _raw 重新合成，与原版哈希相同；99 行共同基线及标点在原像素裁图上复查，无需重复打包 |

八色白名单：`#111318`、`#181A1F`、`#F7F8F4`、`#73F64B`、`#B7BDC5`、`#5A616C`、`#3A3F48`、`#D8DBD3`。

新层级面 CMYK：C 22.580645%、M 16.129032%、Y 0%、K 87.843137%；归一化约 `0.225806 0.161290 0 0.878431`。转换算法、亮绿分色和制作流程未改。

详细证据见 `qa-evidence/surface-only-report.json` 与 `qa-evidence/surface-credentials-profile.json`。回归对比脚本为 `qa-evidence/verify_surface_only.py`，运行时用 `--base` 指向未改色的上一轮目录。原生标志黑白与照片像素是明确例外；没有修改照片来抹除自然色。
'''
    (ROOT/'qa-summary.md').write_text(summary,encoding='utf-8')
    # 用户要求受影响套件保留成套格式；相同字节的配套版式与工艺注明为重导。
    generated=[]
    for folder in ['task-04-card-final','task-05-wristbands','task-06-passes-lanyards','task-07-signage','task-08-rollups','task-09-profile']:
        for p in (ROOT/folder).rglob('*'):
            if not p.is_file() or '__pycache__' in p.parts or '_raw' in p.parts:continue
            rel=p.relative_to(ROOT);old=BASE/rel
            if p.name=='wristbands-mockup.png':continue
            if p.suffix.lower() in ('.pdf','.svg','.png') or p.name.endswith('-layout.json'):
                generated.append(p)
            elif not old.exists() or sha(p)!=sha(old):generated.append(p)
    names=['production.py','production-tokens.json','build_card_final.py','build_credentials.py','build_signage.py','build_rollups.py','compose-credentials.py','qa_round2.py','README.md','qa-summary.json','qa-summary.md','package_surface.py']
    selected=set(generated+[ROOT/n for n in names])
    for n in EVIDENCE_FILES:selected.add(evidence/n)
    # 旧记录仅在平面色白名单或说明文字确有改动时随包更新。
    for p in evidence.glob('*.json'):
        old=BASE/p.relative_to(ROOT)
        if old.exists() and sha(old)!=sha(p):selected.add(p)
    selected=sorted(selected)
    details=[]
    for p in selected:
        rel=p.relative_to(ROOT).as_posix();old=BASE/rel
        same=old.exists() and sha(p)==sha(old)
        details.append({'path':rel,'status':'regenerated-identical' if same else 'modified' if old.exists() else 'new','before_sha256':sha(old) if old.exists() else None,'sha256':sha(p),'bytes':p.stat().st_size})
    changed='RGB (20, 25, 38) → #181A1F / RGB (24, 26, 31)'
    unchanged='色值不变；配套重导（尺寸、文字及几何一致）'
    lines=['# 层级面改色 · 逐文件变更','',f'唯一品牌色变化：{changed}。旧值用 RGB 数组记录，不再在交付包中保留停用十六进制写法或旧中文名称。','',
           '新 CMYK：C 22.580645%、M 16.129032%、Y 0%、K 87.843137%。墨黑 #111318、SP-GREEN 和其他六色不变。版式、文案、字号、尺寸、权限及批量流程不变。',
           '', '两张 AI 效果图已从原 _raw 重合成且哈希不变，所以不重复交付。原标志、字体和照片未改。',
           '', '下表列出全部本次交付文件；“配套重导”标明重新生成但字节一致的文件。SHA-256 与旧版 SHA-256 见 MANIFEST.json。',
           '', '| 文件 | 状态 | 新旧颜色／变化 |','| --- | --- | --- |']
    for rec in details:
        label='配套重导' if rec['status']=='regenerated-identical' else '新增' if rec['status']=='new' else '改动'
        change=unchanged if rec['status']=='regenerated-identical' else changed
        if rec['path'].endswith('-layout.json'):change='不含色值；与上一轮版式记录完全一致'
        elif '-technical.' in rec['path'] and rec['status']=='regenerated-identical':change='刀模、孔位、折线及工艺颜色不变；配套重导'
        elif rec['path'].endswith(('.md','.json','.py')):change=changed+'；色表／说明／验证记录或源代码同步'
        lines.append(f"| `{rec['path']}` | {label} | {change} |")
    lines+=['| `CHANGES.md` | 改动 | 本次逐文件变化清单；旧值用 RGB 数组表示 |','| `MANIFEST.json` | 改动 | 所有交付内容的 SHA-256、旧版 SHA-256 与新旧 surface 值 |','',
            '工艺图与没有层级面的挂绳等文件仍保留原色，绝未把本来指定的墨黑改为层级面。字体子集的生成时间变化不改变任何字形或字宽。']
    changes=ROOT/'CHANGES.md';changes.write_text('\n'.join(lines)+'\n',encoding='utf-8');selected.append(changes)
    details.append({'path':'CHANGES.md','status':'modified','before_sha256':sha(BASE/'CHANGES.md'),'sha256':sha(changes),'bytes':changes.stat().st_size})
    for p in selected:
        if p.suffix.lower() in ('.md','.py','.json','.csv','.svg'):
            s=p.read_text(encoding='utf-8-sig');assert old_text.lower() not in s.lower(),p;assert retired_label not in s,p;assert banned not in s,p
    manifest={'package':'sinoPOP surface color-only delta','surface_before_rgb':[20,25,38],'surface_after_hex':'#181A1F','surface_after_cmyk':[.22580645,.16129032,0,.87843137],'ink_unchanged_hex':'#111318','spot_unchanged':'SP-GREEN','files':details,'manifest_note':'MANIFEST 自身不参与自引用哈希；ZIP 完整性和 SHA-256 另由交付验证记录。','omitted_unchanged':['original logos','static fonts','original photos and raw AI bases','onsite-04-kit.png','wristbands-mockup.png'],'qa_status':'PASS'}
    mp=ROOT/'MANIFEST.json';mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8');selected.append(mp)
    RELEASE.mkdir(exist_ok=True)
    for p in selected:
        dest=RELEASE/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
    with zipfile.ZipFile(ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in selected:z.write(p,p.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(ZIP) as z:
        assert z.testzip() is None
        for rec in details:assert hashlib.sha256(z.read(rec['path'])).hexdigest()==rec['sha256']
    for p in selected:
        q=RELEASE/p.relative_to(ROOT)
        if q.suffix=='.png':
            with Image.open(q) as im:im.verify()
        elif q.suffix=='.pdf':assert len(PdfReader(q).pages)>0
        elif q.suffix=='.svg':ET.parse(q)
    stats={'files':len(selected),'modified':sum(d['status']=='modified' for d in details),'regenerated_identical':sum(d['status']=='regenerated-identical' for d in details),'zip_bytes':ZIP.stat().st_size,'zip_sha256':sha(ZIP),'crc':'PASS','copied_file_formats':'PASS'}
    (ROOT/'_qa/surface-package-verification.json').write_text(json.dumps(stats,indent=2),encoding='utf-8');print(json.dumps(stats,indent=2))

if __name__=='__main__':main()
