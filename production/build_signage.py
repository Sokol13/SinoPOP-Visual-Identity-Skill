from pathlib import Path
import json, math, re, copy
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont
from production import Art, mm, width, export_art, export_technical

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'task-07-signage'
OUT.mkdir(exist_ok=True)
INK, SURFACE, PAPER, GREEN = '#111318', '#181A1F', '#F7F8F4', '#73F64B'
MUTED, SUB, LINE, PALE = '#B7BDC5', '#5A616C', '#3A3F48', '#D8DBD3'
F = TTFont(ROOT / 'assets/fonts/NotoSansSC-Heavy.ttf')
CMAP = F.getBestCmap()
UPM = F['head'].unitsPerEm
HEIGHTS = []
ARTS = {}

def cn(a, x, top, text, min_height, color=PAPER, anchor='start', track=None, size_override=None):
    # 按字面墨迹高度核验汉字；字号本身不等同于实际字高。
    glyphs = [F['glyf'][CMAP[ord(c)]] for c in text if '\u3400' <= c <= '\u9fff']
    ratio = min((g.yMax - g.yMin) / UPM for g in glyphs)
    size = size_override or mm(min_height) / ratio
    baseline = mm(top) + max(g.yMax for g in glyphs) / UPM * size
    a.text(mm(x), baseline, text, size, color, 'ExtraBold', anchor)
    if track:
        HEIGHTS.append({'file': track, 'text': text, 'required_mm': min_height,
                        'minimum_ink_height_mm': round(min((g.yMax-g.yMin)/UPM*size/mm(1) for g in glyphs), 3),
                        'font_pt': round(size, 3), 'width_mm': round(width(text,size,'ExtraBold')/mm(1),3)})
    return size

def tx(a,x,y,s,sz=24,c=PAPER,w='Regular',anchor='start'):
    a.text(mm(x),mm(y),s,sz,c,w,anchor)

def line(a,x,y,x2,y2,c=LINE,sw=1,dash=None):
    a.line(mm(x),mm(y),mm(x2),mm(y2),c,sw,tuple(mm(d) for d in dash) if dash else None)

def rect(a,x,y,w,h,c,r=0,stroke=None,sw=1):
    a.rect(mm(x),mm(y),mm(w),mm(h),c,mm(r),stroke,sw)

def arrow(a,x,y,w=70,h=45,left=False):
    # 箭头使用矢量几何，避免符号字体替换。
    pts=[(0,.35),(0,.65),(.62,.65),(.62,1),(1,.5),(.62,0),(.62,.35)]
    a.poly([(mm(x+(1-px if left else px)*w),mm(y+py*h)) for px,py in pts],GREEN)

def frame(w,h,bg=SURFACE):
    return Art(mm(w),mm(h),bg)

def technical(w,h,holes=None,circle=False,notches=None,folds=None,notes=None):
    a=frame(w,h,PAPER)
    if circle: a.circle(mm(w/2),mm(h/2),mm(w/2),None,INK,.5)
    else: rect(a,0,0,w,h,None,2.1,INK,.5)
    for x,y,r in holes or []: a.circle(mm(x),mm(y),mm(r),None,INK,.5)
    for x,y,r in notches or []: a.circle(mm(x),mm(y),mm(r),None,INK,.5)
    for y in folds or []: line(a,0,y,w,y,SUB,.5,(3,2))
    for i,t in enumerate(notes or []): tx(a,8,12+i*8,t,9,INK,'Regular')
    return a

def emit(stem,a,tech=None,bleed=5):
    ARTS[stem]=a
    export_art([a],OUT,stem,bleed_mm=bleed,preview_long=2400)
    if tech: export_technical([tech],OUT,stem,bleed_mm=bleed)

def restroom_icon(a,x,y):
    for dx in [0,40]:
        a.circle(mm(x+dx+10),mm(y+12),mm(9),PAPER)
        rect(a,x+dx+1,y+27,18,48,PAPER,3)
        rect(a,x+dx+1,y+70,7,34,PAPER,2)
        rect(a,x+dx+12,y+70,7,34,PAPER,2)

def hanging():
    a=frame(1200,300)
    restroom_icon(a,55,94)
    tx(a,190,55,'— 中场',44,PAPER,'Bold');tx(a,368,55,'INTERMISSION',34,MUTED,'Bold')
    cn(a,190,85,'洗手间',104,track='hang-restrooms')
    tx(a,195,247,'RESTROOMS',54,MUTED,'Bold')
    arrow(a,1030,113,115,74)
    emit('hang-restrooms',a,technical(1200,300,holes=[(70,18,3),(1130,18,3)]))
    a=frame(1200,300)
    tx(a,55,69,'04',82,PAPER,'ExtraBold');tx(a,217,64,'B 面',44,PAPER,'Bold')
    cn(a,218,87,'酒水 · 周边',103,track='hang-bar-merch')
    tx(a,222,246,'BAR · MERCH',54,MUTED,'Bold')
    arrow(a,1030,113,115,74)
    emit('hang-bar-merch',a,technical(1200,300,holes=[(70,18,3),(1130,18,3)]))

def entrance():
    a=frame(600,850)
    a.logo(mm(44),mm(44),mm(104),'white')
    tx(a,548,73,'TRACK 01',30,MUTED,'Bold','end')
    tx(a,44,290,'01',250,PAPER,'ExtraBold')
    cn(a,43,359,'入场',157,track='entrance-ticket')
    tx(a,48,609,'DOORS · ENTRANCE',52,MUTED,'Bold')
    arrow(a,458,632,89,60)
    line(a,0,726,600,726,MUTED,2,(9,7))
    tx(a,45,790,'请准备好电子票',38,PAPER,'Bold')
    # 外切线直接沿缺口边缘闭合，不让直线穿过半圆缺口。
    tech=frame(600,850,PAPER)
    pts=[(0,0),(600,0),(600,711)]
    pts += [(600+15*math.cos(math.radians(-90-i*180/100)),726+15*math.sin(math.radians(-90-i*180/100))) for i in range(1,101)]
    pts += [(600,850),(0,850),(0,741)]
    pts += [(15*math.cos(math.radians(90-i*180/100)),726+15*math.sin(math.radians(90-i*180/100))) for i in range(1,101)]
    pts += [(0,0)]
    for p,q in zip(pts,pts[1:]):line(tech,p[0],p[1],q[0],q[1],INK,.5)
    emit('entrance-ticket',a,tech)

def walls():
    a=frame(297,420,PAPER)
    tx(a,23,74,'03',112,INK,'ExtraBold');a.logo(mm(233),mm(28),mm(38),'black')
    arrow(a,25,174,45,30,True)
    cn(a,94,146,'寄存',64,INK,track='wall-coat-check-a3')
    tx(a,96,239,'COAT CHECK',24,MUTED,'Bold')
    line(a,24,327,273,327,PALE,1.5)
    tx(a,24,354,'轻装上阵',26,INK,'Bold')
    tx(a,24,376,'TRAVEL LIGHT',18,MUTED,'Regular')
    emit('wall-coat-check-a3',a,bleed=3)
    a=frame(297,420)
    tx(a,23,72,'06',102,PAPER,'ExtraBold');a.logo(mm(233),mm(27),mm(38),'white')
    tx(a,23,105,'返场',22,PAPER,'Bold');tx(a,86,105,'ENCORE',18,MUTED,'Bold')
    title_size=cn(a,25,146,'出口',63,track='wall-way-out-a3')
    cn(a,25,229,'方向',63,track='wall-way-out-a3',size_override=title_size)
    tx(a,26,343,'WAY OUT',27,MUTED,'Bold')
    arrow(a,226,324,46,30)
    emit('wall-way-out-a3',a,bleed=3)

def pillar_rules():
    a=frame(215.9,279.4,PAPER)
    rect(a,4,4,207.9,271.4,None,2.1,INK,mm(3))
    tx(a,20,35,'01',34,INK,'ExtraBold');a.logo(mm(166),mm(19),mm(28),'black')
    tx(a,20,75,'入场前',21,INK,'Bold');tx(a,20,93,'PRE-SHOW',18,MUTED,'Bold')
    cn(a,20,125,'请出示证件',31,INK,track='pillar-id-letter')
    tx(a,20,181,'ID REQUIRED',27,MUTED,'Bold')
    line(a,20,202,196,202,PALE,1)
    tx(a,20,229,'[年龄限制]',22,INK,'Regular')
    emit('pillar-id-letter',a,bleed=3)
    a=frame(600,900,PAPER)
    rect(a,6,6,588,888,None,2.1,INK,mm(5))
    tx(a,42,57,'01 · 入场前',29,INK,'Bold');tx(a,556,57,'PRE-SHOW',25,MUTED,'Bold','end')
    cn(a,42,100,'入场须知',44,INK,track='house-rules')
    tx(a,43,179,'HOUSE RULES',35,MUTED,'Bold')
    line(a,42,205,558,205,INK,3)
    for i in range(5):
        y=246+i*117
        tx(a,43,y+22,f'{i+1:02}',44,INK,'ExtraBold')
        cn(a,113,y,f'[规则 {i+1:02}]',16,INK,track='house-rules')
        tx(a,115,y+51,f'[RULE {i+1:02}]',23,MUTED,'Regular')
        line(a,43,y+79,557,y+79,PALE,1)
    emit('house-rules',a)

def floors():
    for stem,num,cnword,enword in [('floor-photo-spot','05','站这里拍','PHOTO SPOT'),('floor-queue-start','02','排队起点','QUEUE STARTS HERE')]:
        a=frame(600,600)
        a.circle(mm(300),mm(300),mm(272),None,PAPER,mm(7))
        tx(a,300,181,num,155,PAPER,'ExtraBold','middle')
        cn(a,300,243,cnword,65,PAPER,'middle',stem)
        tx(a,300,382,enword,43,MUTED,'Bold','middle')
        a.logo(mm(270),mm(437),mm(60),'white')
        emit(stem,a,technical(600,600,circle=True))

def table_tent():
    a=frame(148,210)
    tx(a,13,29,'04',39,PAPER,'ExtraBold');tx(a,133,29,'B-SIDE',14,MUTED,'Bold','end')
    a.logo(mm(98),mm(44),mm(35),'white')
    cn(a,13,94,'周边',31,PAPER,track='table-merch-a5')
    tx(a,14,143,'MERCH',25,MUTED,'Bold')
    line(a,14,158,134,158,LINE,1)
    tx(a,14,179,'[商品] · USD [00]',11,PAPER,'Regular')
    tx(a,14,195,'[ITEM]',9,MUTED,'Regular')
    ARTS['table-merch-a5-panel']=a
    # 两个 A5 面板与底座、粘口连成一张，首面旋转以便两面顶部在屋脊会合。
    spread=frame(148,515)
    spread.place(a,0,0,rotation=180)
    spread.place(a,0,mm(210))
    rect(spread,0,500,148,15,PAPER)
    emit('table-merch-a5',spread,technical(148,515,folds=[210,420,500]))
    # 正面可编辑单张仅供快速改价与审稿，不重复输出独立印刷面。
    a.svg(OUT/'table-merch-a5-panel.svg')

def overview():
    # 总览按同一比例展示实物，标签另排，不作为量产印刷面。
    from xml.etree import ElementTree as ET
    NS='http://www.w3.org/2000/svg'
    ET.register_namespace('',NS)
    W,H=3600,2300
    s=.95
    canvas=Image.new('RGB',(W,H),PAPER)
    d=ImageDraw.Draw(canvas)
    cnfont=ImageFont.truetype(str(ROOT/'assets/fonts/NotoSansSC-Heavy.ttf'),45)
    enfont=ImageFont.truetype(str(ROOT/'assets/fonts/Archivo-Bold.ttf'),29)
    d.text((85,105),'现场标识 · 歌单',font=cnfont,fill=INK,anchor='ls')
    d.text((85,159),'SIGN FAMILY / ONE PHYSICAL SCALE',font=enfont,fill=SUB,anchor='ls')
    svg=ET.Element('{'+NS+'}svg',{'width':str(W),'height':str(H),'viewBox':f'0 0 {W} {H}'})
    ET.SubElement(svg,'{'+NS+'}rect',{'width':str(W),'height':str(H),'fill':PAPER})
    placements=[('hang-restrooms',85,780,'吊挂 120 × 30 cm'),('hang-bar-merch',85,1120,'吊挂 120 × 30 cm'),
                ('entrance-ticket',1350,280,'入口 60 × 85 cm'),('house-rules',2010,235,'须知 60 × 90 cm'),
                ('floor-photo-spot',2690,505,'地贴 Ø 60 cm'),('floor-queue-start',2690,1305,'地贴 Ø 60 cm'),
                ('wall-coat-check-a3',85,1610,'墙贴 A3'),('wall-way-out-a3',440,1610,'墙贴 A3'),
                ('pillar-id-letter',820,1743,'立柱 Letter'),('table-merch-a5-panel',1110,1807,'桌卡 A5')]
    for stem,x,y,label in placements:
        a=ARTS[stem]; w=a.w/mm(1)*s;h=a.h/mm(1)*s
        p=OUT/(stem+'-preview.png')
        if stem=='table-merch-a5-panel':
            # 成品面板从展开页正面裁出，预览不含背板与粘口。
            im=Image.open(OUT/'table-merch-a5-preview.png').convert('RGB')
            im=im.crop((0,round(im.height*210/515),im.width,round(im.height*420/515)))
        else: im=Image.open(p).convert('RGB')
        thumb=im.resize((round(w),round(h)),Image.Resampling.LANCZOS)
        if stem.startswith('floor-'):
            mask=Image.new('L',thumb.size,0);ImageDraw.Draw(mask).ellipse((0,0,thumb.width-1,thumb.height-1),fill=255)
            canvas.paste(thumb,(round(x),round(y)),mask)
        else:canvas.paste(thumb,(round(x),round(y)))
        d.text((x,y+h+48),label,font=enfont if not any('\u3400'<=c<='\u9fff' for c in label) else ImageFont.truetype(str(ROOT/'assets/fonts/NotoSansSC-Bold.ttf'),25),fill=INK,anchor='ls')
        child=ET.parse(OUT/(stem+'.svg')).getroot()
        child.set('x',str(x));child.set('y',str(y));child.set('width',str(w));child.set('height',str(h))
        if stem.startswith('floor-'):
            defs=ET.SubElement(svg,'{'+NS+'}defs');clip=ET.SubElement(defs,'{'+NS+'}clipPath',{'id':stem+'-cut'})
            ET.SubElement(clip,'{'+NS+'}circle',{'cx':str(x+w/2),'cy':str(y+h/2),'r':str(w/2)})
            group=ET.SubElement(svg,'{'+NS+'}g',{'clip-path':'url(#'+stem+'-cut)'});group.append(child)
        else:svg.append(child)
    # 总览文字也由生产字体绘制，SVG 字体嵌入沿用引擎。
    lab=Art(W,H,PAPER);lab.ops=[]
    lab.text(85,105,'现场标识 · 歌单',45,INK,'ExtraBold')
    lab.text(85,159,'SIGN FAMILY / ONE PHYSICAL SCALE',29,SUB,'Bold')
    for stem,x,y,label in placements:lab.text(x,y+ARTS[stem].h/mm(1)*s+48,label,25,INK,'Bold')
    lp=OUT/'_overview-labels.svg';lab.svg(lp)
    lr=ET.parse(lp).getroot()
    for el in list(lr):svg.append(el)
    lp.unlink()
    ET.ElementTree(svg).write(OUT/'sign-family-overview.svg',encoding='utf-8',xml_declaration=True)
    canvas.save(OUT/'sign-family-overview.png')

def main():
    hanging();entrance();walls();pillar_rules();floors();table_tent();overview()
    (OUT/'signage-height-qa.json').write_text(json.dumps(HEIGHTS,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'README.md').write_text('''# 现场标识生产文件

每个物料的 `-rgb.pdf` 是 RGB 打样稿，`-print.pdf` 是 CMYK + SP-GREEN 专色印刷稿；同名 SVG 可编辑文字并嵌入字体子集，`-preview.png` 是 2400 px 长边预览。只有箭头使用亮绿，其他编号与环线为纸白或墨黑。深色大面板统一为层级面 #181A1F（墨黑提亮 3%）。英文使用灰色全大写。

| 文件前缀 | 成品尺寸 | 出血 | 工艺 |
|---|---:|---:|---|
| hang-restrooms / hang-bar-merch | 1200 × 300 mm | 5 mm | 技术 PDF 含外切与两枚直径 6 mm 吊孔；孔心距侧边 70 mm、距顶边 18 mm |
| entrance-ticket | 600 × 850 mm | 5 mm | 技术 PDF 含外切与两侧直径 30 mm 半圆缺口；印刷虚线是票根视觉语言 |
| wall-coat-check-a3 / wall-way-out-a3 | 297 × 420 mm | 3 mm | 直裁 |
| pillar-id-letter | 215.9 × 279.4 mm | 3 mm | 直裁 |
| house-rules | 600 × 900 mm | 5 mm | 直裁 |
| floor-photo-spot / floor-queue-start | 直径 600 mm | 5 mm | 技术 PDF 为圆形外切，方形 PDF 的 TrimBox 是外接框 |
| table-merch-a5 | 展开 148 × 515 mm；每面 148 × 210 mm | 5 mm | 双 A5 面板 210 + 210 mm，底座 80 mm，粘口 15 mm；首面在展开拼版中旋转 180°，两面顶部同在 y=210 mm 的屋脊折线；另两折线 y=420/500 mm |

`table-merch-a5-panel.svg` 是桌卡正面编辑副本；正式生产使用展开印刷 PDF。`sign-family-overview.svg/png` 为同物理比例的家族总览，只作审稿，不作为工厂尺寸依据。

`signage-height-qa.json` 记录每项功能词的实际汉字墨迹高度，依据 Noto Sans SC Heavy 字形边界计算。吊挂至少 100 mm、入口至少 150 mm、A3 墙贴至少 60 mm、Letter 立柱至少 30 mm、须知标题至少 40 mm/正文至少 15 mm、地贴至少 60 mm、桌卡至少 15 mm。辅助编号与英文不替代功能词。

须知五条规则、年龄限制、桌卡商品和价格全部是方括号占位；未填写任何活动日期或场地。切线、吊孔、折线只放在技术 PDF，印刷面没有工程线。亮绿建议用荧光专色 SP-GREEN，需实物打样比对；无任何供应商色号。墨黑或层级面材料上的纸白印刷要由印厂制作白墨版。方向牌仅用于运营导向，法定疏散标识沿用场馆已有设施。
''',encoding='utf-8')
    print('signage complete',len(ARTS),len(HEIGHTS))

if __name__=='__main__':main()
