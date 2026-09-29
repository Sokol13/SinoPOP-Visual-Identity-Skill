from pathlib import Path
import json
from production import Art, mm, export_art, export_technical

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'task-08-rollups';OUT.mkdir(exist_ok=True)
INK,SURFACE,PAPER,GREEN='#111318','#181A1F','#F7F8F4','#73F64B'
MUTED,SUB,LINE,PALE='#B7BDC5','#5A616C','#3A3F48','#D8DBD3'

def tx(a,x,y,s,size,c=PAPER,weight='Regular',anchor='start'):
    a.text(mm(x),mm(y),s,size,c,weight,anchor)
def rect(a,x,y,w,h,c,r=0,stroke=None,sw=1):
    a.rect(mm(x),mm(y),mm(w),mm(h),c,mm(r),stroke,sw)
def line(a,x,y,x2,y2,c=LINE,sw=1,dash=None):
    a.line(mm(x),mm(y),mm(x2),mm(y2),c,sw,tuple(mm(v) for v in dash) if dash else None)
def emit(stem,a):
    export_art([a],OUT,stem,bleed_mm=5,preview_long=3000)
    t=Art(mm(850),mm(2000),PAPER)
    rect(t,0,0,850,2000,None,0,INK,.5)
    line(t,0,1850,850,1850,SUB,.75,(8,5))
    tx(t,35,1900,'底部 150 mm 收卷区 · 不放内容',24,INK,'Bold')
    tx(t,35,1940,'RETRACTABLE BASE / KEEP CLEAR',18,SUB)
    tx(t,35,80,'成品 850 × 2000 mm · 四边出血 5 mm',24,INK,'Bold')
    export_technical([t],OUT,stem,bleed_mm=5)

def ticket():
    a=Art(mm(850),mm(2000),SURFACE)
    a.logo(mm(65),mm(75),mm(210),'white')
    tx(a,777,115,'No. [场次]',33,MUTED,'Bold','end')
    tx(a,65,487,'入场 · TRACK 01',56,GREEN,'Bold')
    for y,s in [(705,'欢迎'),(938,'来到'),(1171,'现场')]:
        tx(a,57,y,s,530,PAPER,'ExtraBold')
    tx(a,66,1300,'WELCOME',104,MUTED,'Bold')
    tx(a,66,1410,'TO THE SHOW',104,MUTED,'Bold')
    rect(a,0,1540,850,310,GREEN)
    line(a,0,1540,850,1540,INK,2,(11,8))
    # 两侧半圆为票根印刷语言；卷帘纸面保持完整。
    a.circle(0,mm(1540),mm(19),SURFACE);a.circle(mm(850),mm(1540),mm(19),SURFACE)
    tx(a,62,1631,'留个纪念',46,INK,'Bold')
    tx(a,62,1673,'KEEP THIS STUB',32,INK,'Bold')
    tx(a,60,1772,'sinopop.us',89,INK,'Bold')
    rect(a,622,1610,166,166,INK,2.1)
    tx(a,705,1692,'[二维码]',22,PAPER,'Regular','middle')
    tx(a,705,1723,'[QR]',18,PAPER,'Regular','middle')
    emit('rollup-a-ticket',a)

def setlist():
    a=Art(mm(850),mm(2000),SURFACE)
    rect(a,46,111,758,1669,PAPER,2.1)
    a.poly([(mm(x),mm(y)) for x,y in [(267,54),(580,68),(572,88),(582,107),(574,128),(584,149),(273,143),(278,121),(268,98),(276,78)]],GREEN)
    tx(a,105,296,'今晚的',232,INK,'ExtraBold')
    tx(a,105,414,'歌单',232,INK,'ExtraBold')
    tx(a,109,480,"TONIGHT'S SETLIST",60,SUB,'Bold')
    line(a,105,520,746,520,INK,7)
    rows=[('01','入场','DOORS'),('02','验票','CHECK-IN'),('03','寄存','COAT CHECK'),
          ('04','酒水 · 周边','BAR · B-SIDE'),('05','演出','THE SHOW'),
          ('—','中场 · 洗手间','INTERMISSION'),('06','返场 · 出口','ENCORE · WAY OUT')]
    for i,(num,cn,en) in enumerate(rows):
        y=626+i*139
        if num=='05':rect(a,88,y-73,674,120,GREEN,2.1)
        col=SUB if num=='—' else INK
        tx(a,112,y,num,97,col,'ExtraBold')
        tx(a,245,y-2,cn,61,col,'Bold')
        tx(a,248,y+35,en,30,col,'Bold')
    line(a,105,1553,746,1553,PALE,2)
    rect(a,99,1621,650,98,None,2.1,SUB,1)
    tx(a,121,1657,'[艺人名] · [MM.DD]',27,INK)
    tx(a,121,1695,'[每场更换贴纸]',21,SUB)
    a.logo(mm(653),mm(1640),mm(63),'black')
    emit('rollup-b-setlist',a)

def playing():
    a=Art(mm(850),mm(2000),SURFACE)
    a.poly([(mm(61),mm(119)),(mm(61),mm(149)),(mm(88),mm(134))],GREEN)
    tx(a,111,147,'正在上演 · NOW PLAYING',48,GREEN,'Bold')
    a.logo(mm(685),mm(62),mm(108),'white')
    # 专辑框保持完全空白；使用说明排在框外，之后放入获授权原图。
    rect(a,65,278,720,720,None,2.1,LINE,3)
    tx(a,66,1046,'艺人海报原图整张放入，',30,MUTED,'Regular')
    tx(a,66,1085,'不裁切不压字',30,MUTED,'Regular')
    tx(a,62,1213,'[艺人名]',165,PAPER,'ExtraBold')
    tx(a,67,1266,'[ARTIST]',43,MUTED,'Bold')
    line(a,67,1328,785,1328,LINE,10)
    line(a,67,1328,340,1328,GREEN,10)
    a.circle(mm(340),mm(1328),mm(18),GREEN)
    tx(a,67,1390,'[00:00]',35,MUTED,'Bold')
    tx(a,783,1390,'[MM.DD]',35,MUTED,'Bold','end')
    a.circle(mm(425),mm(1520),mm(102),GREEN)
    a.poly([(mm(402),mm(1473)),(mm(402),mm(1567)),(mm(475),mm(1520))],INK)
    # 前后切换键只用无歧义的矢量图形。
    rect(a,162,1494,8,52,MUTED)
    a.poly([(mm(216),mm(1494)),(mm(216),mm(1546)),(mm(173),mm(1520))],MUTED)
    rect(a,680,1494,8,52,MUTED)
    a.poly([(mm(634),mm(1494)),(mm(634),mm(1546)),(mm(677),mm(1520))],MUTED)
    line(a,65,1696,785,1696,LINE,2)
    a.logo(mm(67),mm(1737),mm(91),'white')
    tx(a,188,1760,'主办方',28,PAPER,'Bold');tx(a,188,1792,'PRESENTED BY',20,MUTED,'Bold')
    tx(a,785,1790,'sinopop.us',51,MUTED,'Bold','end')
    emit('rollup-c-now-playing',a)

def main():
    ticket();setlist();playing()
    (OUT/'README.md').write_text('''# 易拉宝生产文件

三款成品均为 850 × 2000 mm，1:1 矢量 PDF，四边 5 mm 出血。底部 y=1850–2000 mm 是 150 mm 收卷区，仅延续层级面底色，不含文字、标志、二维码或图案。

| 文件前缀 | 内容 |
|---|---|
| rollup-a-ticket | 欢迎票根；二维码是无链接的方括号占位；下方票根区在收卷区上方结束 |
| rollup-b-setlist | 纸白歌单、印刷撕边绿胶带、01–06 与中场；05 亮绿色块；底部每场可更换贴纸区 |
| rollup-c-now-playing | 完全空白的专辑框；整张原图置入说明在框外；艺人、日期与播放时间皆占位 |

每款 `-rgb.pdf` 为 RGB 打样，`-print.pdf` 为 CMYK + SP-GREEN 专色生产文件，`-technical.pdf` 只显示尺寸、收卷边界及说明，不作为印刷面。SVG 为可编辑文字源文件，已嵌入真实字体子集及原始标志 SVG；预览 PNG 长边 3000 px。

主办信息只使用品牌名与 sinopop.us，不编造任何演出。节目、艺人、日期、场次、二维码均待提供真实内容后替换。亮绿建议用荧光专色，需实物打样比对；SP-GREEN 由印厂匹配，不预设供应商色号。若使用深色基材，纸白文字和白标须另制白墨版。卷轴机械规格应由所用展架供应商确认，图文保持在既定收卷区之上。
''',encoding='utf-8')
    print('rollups complete')

if __name__=='__main__':main()
