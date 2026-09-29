from pathlib import Path
import base64, json, re, shutil, hashlib, io
from xml.sax.saxutils import escape
from fontTools.ttLib import TTFont as FTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools import subset
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject
import pymupdf
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
ASSET=ROOT/'assets'; ASSET.mkdir(exist_ok=True)
FONTS=ASSET/'fonts'; FONTS.mkdir(exist_ok=True)
SRC=ROOT/'_source'/'sinopop-design-system'
OLD=ROOT.parent/'sinopop-promoter-visual'/'research'/'fonts'/'sources'
INK='#111318'; SURFACE='#1B1E24'; PAPER='#F7F8F4'; GREEN='#73F64B'; MUTED='#B7BDC5'; SUB='#5A616C'; LINE='#3A3F48'; PALE='#D8DBD3'
PALETTE=[INK,SURFACE,PAPER,GREEN,MUTED,SUB,LINE,PALE]
for v in ['black','white']:
    source_logo=SRC/'assets'/f'sinopop-logo-{v}.svg'
    if source_logo.exists(): shutil.copy2(source_logo,ASSET/f'sinopop-logo-{v}.svg')

def fonts():
    specs=[('Archivo-Regular','archivo','Archivo[wdth,wght].ttf',400),('Archivo-Bold','archivo','Archivo[wdth,wght].ttf',700),('Archivo-ExtraBold','archivo','Archivo[wdth,wght].ttf',800),('NotoSansSC-Regular','notosanssc','NotoSansSC[wght].ttf',400),('NotoSansSC-Medium','notosanssc','NotoSansSC[wght].ttf',500),('NotoSansSC-Bold','notosanssc','NotoSansSC[wght].ttf',700),('NotoSansSC-Heavy','notosanssc','NotoSansSC[wght].ttf',900)]
    for name,folder,source,weight in specs:
        dst=FONTS/(name+'.ttf')
        if not dst.exists():
            f=FTFont(OLD/folder/source)
            axes={'wght':weight}
            if any(a.axisTag=='wdth' for a in f['fvar'].axes): axes['wdth']=100
            f=instantiateVariableFont(f,axes,inplace=True)
            for rec in f['name'].names:
                if rec.nameID in [1,4,6]: rec.string=name.encode(rec.getEncoding(),errors='replace')
            f.save(dst)
        pdfmetrics.registerFont(TTFont(name,str(dst)))
        lic=OLD/folder/'OFL.txt'
        if lic.exists(): shutil.copy2(lic,FONTS/(folder+'-OFL.txt'))
fonts()
ALL_CHARS=''.join(chr(i) for i in range(32,127))+'姓名微信号电话邮箱入场歌单今晚的正在播放上演欢迎来到现场演出验票寄存酒水周边中场洗手间返场出口方向站这里拍普通贵宾工作人员艺人嘉宾轻装上阵主办方介绍曲目联系方式后台通行证音乐实物内卡封套正面背面唱片压凹折页模切刷边工艺展开中国北美青年文化票根留个纪念流程示意未确认嘉宾取票散场放映主控绿色姓名胶带'
ALL_CHARS+=' · +1 [000 000 0000] name@sinopop.us First Last Title Team No. 0001 TONIGHT\'S SETLIST SIDE A ALL ACCESS ADMIT ONE ▶ → ←'
CSS=''
for name in ['Archivo-Regular','Archivo-Bold','Archivo-ExtraBold','NotoSansSC-Regular','NotoSansSC-Medium','NotoSansSC-Bold','NotoSansSC-Heavy']:
    f=FTFont(FONTS/(name+'.ttf'))
    opts=subset.Options(); opts.layout_features=['*']; ss=subset.Subsetter(options=opts); ss.populate(text=ALL_CHARS); ss.subset(f)
    f.flavor='woff2'; b=io.BytesIO(); f.save(b)
    CSS+=f"@font-face{{font-family:'{name}';src:url(data:font/woff2;base64,{base64.b64encode(b.getvalue()).decode()}) format('woff2');}}\n"
LOGOS={v:base64.b64encode((ASSET/f'sinopop-logo-{v}.svg').read_bytes()).decode() for v in ['black','white']}
DRAWINGS={v:svg2rlg(str(ASSET/f'sinopop-logo-{v}.svg')) for v in ['black','white']}
QA=[]

def runs(s,weight):
    arr=[]
    for ch in s:
        # 小号中文跟随同行英文字重；ExtraBold 用于大号姓名和标题，对应中文 Heavy。
        chinese_weight={'Regular':'Regular','Medium':'Medium','Bold':'Bold','ExtraBold':'Heavy'}[weight]
        font='NotoSansSC-'+chinese_weight if ord(ch)>255 and ch not in '→←▶' else 'Archivo-'+weight
        if arr and arr[-1][0]==font: arr[-1]=(font,arr[-1][1]+ch)
        else: arr.append((font,ch))
    return arr
def width(s,size,weight='Regular'):
    return sum(pdfmetrics.stringWidth(t,f,size) for f,t in runs(s,weight))

class Art:
    def __init__(self,w=252,h=144,bg=INK): self.w=w; self.h=h; self.bg=bg; self.ops=[]; self.rect(0,0,w,h,bg)
    def rect(self,x,y,w,h,c,r=0,stroke=None,sw=1): self.ops.append(('rect',x,y,w,h,c,r,stroke,sw))
    def circle(self,x,y,r,c,stroke=None,sw=1): self.ops.append(('circle',x,y,r,c,stroke,sw))
    def line(self,x,y,x2,y2,c=LINE,sw=1,dash=None): self.ops.append(('line',x,y,x2,y2,c,sw,dash))
    def poly(self,pts,c): self.ops.append(('poly',pts,c))
    def text(self,x,y,s,size=7.5,c=PAPER,weight='Regular',anchor='start',maxw=None):
        if maxw and width(s,size,weight)>maxw: raise ValueError(f'Text overflow {s}: {width(s,size,weight)} > {maxw}')
        if size<7: raise ValueError(f'Font below 7pt: {s}')
        self.ops.append(('text',x,y,s,size,c,weight,anchor))
    def logo(self,x,y,w=60,v='white'): self.ops.append(('logo',x,y,w,v))
    def svg(self,path):
        out=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{self.w/72:.8f}in" height="{self.h/72:.8f}in" viewBox="0 0 {self.w} {self.h}"><defs><style>{CSS}</style></defs>']
        for op in self.ops:
            t,*v=op
            if t=='rect':
                x,y,w,h,c,r,st,sw=v; out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{c or "none"}" stroke="{st or "none"}" stroke-width="{sw}"/>')
            elif t=='circle':
                x,y,r,c,st,sw=v; out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c or "none"}" stroke="{st or "none"}" stroke-width="{sw}"/>')
            elif t=='line':
                x,y,x2,y2,c,sw,dash=v; out.append(f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{sw}"'+(f' stroke-dasharray="{dash[0]} {dash[1]}"' if dash else '')+'/>')
            elif t=='poly': out.append(f'<polygon points="'+ ' '.join(f'{x},{y}' for x,y in v[0])+f'" fill="{v[1]}"/>')
            elif t=='text':
                x,y,s,sz,c,weight,anc=v; xx=x-(width(s,sz,weight) if anc=='end' else width(s,sz,weight)/2 if anc=='middle' else 0)
                for font,txt in runs(s,weight):
                    out.append(f'<text x="{xx:.4f}" y="{y}" font-family="{font}" font-size="{sz}" fill="{c}">{escape(txt)}</text>'); xx+=pdfmetrics.stringWidth(txt,font,sz)
            elif t=='logo':
                x,y,w,var=v; out.append(f'<image x="{x}" y="{y}" width="{w}" height="{w*1741/2315}" preserveAspectRatio="xMidYMid meet" xlink:href="data:image/svg+xml;base64,{LOGOS[var]}"/>')
        out.append('</svg>'); Path(path).write_text('\n'.join(out),encoding='utf-8')
    def pdfdraw(self,c,ox=0,oy=0,sx=1,sy=1):
        c.saveState(); c.translate(ox,oy); c.scale(sx,sy)
        for op in self.ops:
            t,*v=op
            if t=='rect':
                x,y,w,h,fill,r,st,sw=v
                if fill:c.setFillColor(HexColor(fill))
                if st:c.setStrokeColor(HexColor(st)); c.setLineWidth(sw)
                c.roundRect(x,self.h-y-h,w,h,r,stroke=int(bool(st)),fill=int(bool(fill)))
            elif t=='circle':
                x,y,r,fill,st,sw=v
                if fill:c.setFillColor(HexColor(fill))
                if st:c.setStrokeColor(HexColor(st));c.setLineWidth(sw)
                c.circle(x,self.h-y,r,stroke=int(bool(st)),fill=int(bool(fill)))
            elif t=='line':
                x,y,x2,y2,col,sw,dash=v;c.setStrokeColor(HexColor(col));c.setLineWidth(sw);c.setDash(dash or []);c.line(x,self.h-y,x2,self.h-y2);c.setDash([])
            elif t=='poly':
                pts,col=v; p=c.beginPath();p.moveTo(pts[0][0],self.h-pts[0][1])
                for x,y in pts[1:]:p.lineTo(x,self.h-y)
                p.close();c.setFillColor(HexColor(col));c.drawPath(p,fill=1,stroke=0)
            elif t=='text':
                x,y,s,sz,col,we,anc=v;x-=width(s,sz,we) if anc=='end' else width(s,sz,we)/2 if anc=='middle' else 0;c.setFillColor(HexColor(col))
                for f,txt in runs(s,we):c.setFont(f,sz);c.drawString(x,self.h-y,txt);x+=pdfmetrics.stringWidth(txt,f,sz)
            elif t=='logo':
                x,y,w,var=v;d=DRAWINGS[var];c.saveState();c.translate(x,self.h-y-w*1741/2315);c.scale(w/d.width,w/d.width);renderPDF.draw(d,c,0,0);c.restoreState()
        c.restoreState()

def identity(a,x=14,y=31,c=PAPER):
    a.text(x,y,'[姓名]',22,c,'ExtraBold');a.text(x,y+15,'First Last',10,c,'Bold');a.text(x,y+29,'Title · Team',7.5,MUTED if c==PAPER else SUB)
def contacts(a,x=14,y=84,c=PAPER,dy=12):
    for i,s in enumerate(['+1 [000 000 0000]','WeChat [微信号]','name@sinopop.us','sinopop.us']): a.text(x,y+dy*i,s,7.5,c,maxw=a.w-x-12)
def logo_face(n,label):
    a=Art();a.logo(18,20,82);a.text(18,126,label,7.5,MUTED,'Bold');a.text(236,129,n,60,GREEN,'ExtraBold','end');return a

def ticket():
    f=Art();b=Art()
    for a in [f,b]:
        a.rect(168,0,84,144,GREEN);a.line(168,8,168,136,INK,.7,(2,2));a.circle(168,0,6,PAPER);a.circle(168,144,6,PAPER)
        a.text(181,28,'入场',16,INK,'ExtraBold');a.text(181,42,'ADMIT ONE',7.5,INK,'Bold');a.line(181,52,238,52,INK,.7)
        a.text(181,127,'No. 0001',8,INK,'Bold')
        for i in range(24): a.rect(181+i*2.25,76,.6+(i%3)*.25,27,INK)
    f.logo(16,18,75);f.text(15,130,'01',51,GREEN,'ExtraBold')
    identity(b,13,31);contacts(b,13,85,dy=12)
    return f,b
def setlist():
    f=Art(bg=PAPER);b=Art()
    f.poly([(73,0),(181,0),(178,7),(181,11),(178,16),(75,14),(77,10),(73,6)],GREEN)
    f.line(13,24,239,24,INK,2);f.text(13,49,'[姓名]',21,INK,'ExtraBold');f.text(100,48,'First Last',9,INK,'Bold');f.text(238,48,'Title · Team',7,INK,anchor='end')
    rows=[('电话 PHONE','+1 [000 000 0000]'),('微信 WECHAT','[微信号]'),('邮箱 EMAIL','name@sinopop.us'),('sinopop.us','')]
    for i,(lab,val) in enumerate(rows):
        y=69+i*18;f.text(13,y,f'{i+1:02}',10,INK,'ExtraBold');f.text(34,y,lab,7.5,INK,'Bold');f.text(238,y,val,7.5,INK,anchor='end');f.line(13,y+6,239,y+6,PALE,.5)
    b.logo(79,20,94);b.line(16,105,236,105,GREEN,2);b.text(126,125,"TONIGHT'S SETLIST",9,PAPER,'Bold','middle')
    return f,b
def vinyl():
    f=Art();b=Art()
    f.logo(12,11,43);f.circle(175,72,59,GREEN)
    for r in [54,49,44,39,34]:f.circle(175,72,r,None,INK,.6)
    f.circle(175,72,27,INK);f.text(175,70,'SIDE A',8,GREEN,'Bold','middle');f.text(175,82,'sinoPOP',8,PAPER,'Bold','middle');f.circle(175,94,2,GREEN)
    f.text(14,124,'03',32,GREEN,'ExtraBold');identity(b);contacts(b)
    b.circle(236,16,7,GREEN)
    return f,b
def backstage():
    f=Art(144,252);b=Art(144,252)
    for a in [f,b]:
        a.ops[0]=('rect',0,0,144,252,INK,6,None,1)
        a.rect(55,11,34,5,PAPER,r=2.5)
    f.logo(46,26,52);f.text(14,107,'[姓名]',24,PAPER,'ExtraBold');f.text(14,124,'First Last',10,PAPER,'Bold');f.text(14,139,'Title · Team',7.5,MUTED)
    f.rect(0,151,144,32,GREEN);f.text(72,172,'主办方 PROMOTER',11.5,INK,'ExtraBold','middle',maxw=124);contacts(f,14,200,dy=12)
    b.logo(24,69,96);b.text(72,234,'sinopop.us',8,MUTED,'Bold','middle')
    return f,b
def jcard():
    f=Art();b=Art(bg=PAPER)
    f.line(15,17,236,17,GREEN,2);f.logo(75,27,102);f.text(14,127,'SIDE A',8,MUTED,'Bold');f.text(238,127,'05',17,GREEN,'ExtraBold','end')
    b.text(14,27,'[姓名]',17,INK,'ExtraBold');b.text(92,26,'First Last',9,INK,'Bold');b.text(238,26,'Title · Team',7,INK,anchor='end');b.line(14,37,238,37,INK,1.5)
    for i,s in enumerate(['+1 [000 000 0000]','WeChat [微信号]','name@sinopop.us','sinopop.us']):
        y=57+i*23;b.text(14,y,f'{i+1:02}',11,INK,'ExtraBold');b.text(42,y,s,8,INK);b.line(14,y+8,238,y+8,PALE,.5)
    return f,b
def material():
    f=Art();b=Art()
    f.text(17,68,'[姓名]',29,LINE,'ExtraBold');f.text(18,87,'First Last',10,LINE,'Bold');f.logo(199,16,36);f.line(18,121,233,121,GREEN,1)
    b.logo(188,17,47);b.text(16,31,'[姓名]',16,PAPER,'ExtraBold');b.text(16,46,'First Last',9,PAPER,'Bold');b.text(16,60,'Title · Team',7.5,MUTED);contacts(b,16,85,dy=12)
    return f,b

def printpdf(arts,path,alternative=False):
    tmp=Path(path).with_suffix('.raw.pdf');c=canvas.Canvas(str(tmp),pageCompression=1);boxes=[]
    for a in arts:
        W,H=a.w,a.h
        if alternative:
            W,H=(54*72/25.4,90*72/25.4) if a.h>a.w else (90*72/25.4,54*72/25.4)
        # 出血为 9pt，外侧再留 9pt 安放裁切线。
        m=18; bleed=9;c.setPageSize((W+36,H+36));c.setFillColor(HexColor(PAPER));c.rect(0,0,W+36,H+36,fill=1,stroke=0)
        c.setFillColor(HexColor(a.bg));c.rect(9,9,W+18,H+18,fill=1,stroke=0)
        # 将碰到裁边的色块延伸至出血区，不缩放内部标志。
        for op in a.ops:
            if op[0]=='rect':
                _,x,y,w,h,fill,r,st,sw=op
                if fill and (x==0 or y==0 or x+w==a.w or y+h==a.h):
                    x0=18+x*W/a.w-(9 if x==0 else 0);y0=18+(a.h-y-h)*H/a.h-(9 if y+h==a.h else 0)
                    ww=w*W/a.w+(9 if x==0 else 0)+(9 if x+w==a.w else 0);hh=h*H/a.h+(9 if y==0 else 0)+(9 if y+h==a.h else 0)
                    c.setFillColor(HexColor(fill));c.rect(x0,y0,ww,hh,fill=1,stroke=0)
        if alternative:
            # 替代尺寸使用原比例等比居中；避免把真标志非等比拉伸。
            sc=min(W/a.w,H/a.h);a.pdfdraw(c,18+(W-a.w*sc)/2,18+(H-a.h*sc)/2,sc,sc)
        else:a.pdfdraw(c,18,18)
        c.setStrokeColor(HexColor(INK));c.setLineWidth(.25)
        for x in [18,18+W]:
            c.line(x,2,x,7);c.line(x,H+29,x,H+34)
        for y in [18,18+H]:
            c.line(2,y,7,y);c.line(W+29,y,W+34,y)
        boxes.append((W,H));c.showPage()
    c.save();reader=PdfReader(str(tmp));writer=PdfWriter()
    for p,(W,H) in zip(reader.pages,boxes):
        p.trimbox=RectangleObject([18,18,18+W,18+H]);p.bleedbox=RectangleObject([9,9,27+W,27+H]);writer.add_page(p)
    writer.add_metadata({'/Title':'sinoPOP | Music objects | Concept print master','/Subject':'RGB concept print artwork; 0.125 in bleed; embedded licensed fonts','/Creator':'sinoPOP visual production'})
    with open(path,'wb') as fp:writer.write(fp)
    tmp.unlink()

def spread_jcard(f,b):
    # 折后封面 88.9 × 50.8mm；脊 12.7mm；背折翼 38.1mm。
    out=Art(396,144);ins=Art(396,144,bg=PAPER)
    for target,a,offset in [(out,f,144),(ins,b,0)]:
        for op in a.ops:
            t,*v=op
            if t in ['rect','circle','text','logo']:v[0]+=offset
            elif t=='line':v[0]+=offset;v[2]+=offset
            elif t=='poly':v[0]=[(x+offset,y) for x,y in v[0]]
            target.ops.append((t,*v))
    out.text(15,27,'SIDE B',9,GREEN,'Bold');out.text(15,121,'sinopop.us',8,PAPER,'Bold');out.logo(19,47,62)
    for i,ch in enumerate('[姓名]'):out.text(126,43+i*18,ch,13,PAPER,'ExtraBold','middle')
    ins.text(310,55,'音乐实物',15,INK,'ExtraBold','middle');ins.text(310,78,'SIDE A / SIDE B',8,INK,'Bold','middle');ins.text(310,120,'sinopop.us',8,INK,'Bold','middle')
    return out,ins

DIRS=['01-ticket','02-setlist','03-vinyl','04-backstage','05-jcard','06-material']
BUILDERS=[ticket,setlist,vinyl,backstage,jcard,material]
def main():
    thumbs=[]
    for name,fn in zip(DIRS,BUILDERS):
        folder=ROOT/'task-01-cards'/name;folder.mkdir(parents=True,exist_ok=True);f,b=fn();f.svg(folder/'front.svg');b.svg(folder/'back.svg')
        arts=[f,b]
        if name=='05-jcard':
            o,i=spread_jcard(f,b);o.svg(folder/'spread-outside.svg');i.svg(folder/'spread-inside.svg');printpdf([o,i],folder/'construction.pdf')
        if name=='03-vinyl':
            # 沿用已经确认的缩进内卡尺寸与圆窗位置，避免回退到早期版本。
            inner=Art(246.3307,138.3307,GREEN);cx,cy=172.16535,69.16535
            for r in [59,54,49,44,39,34]:inner.circle(cx,cy,r,None,INK,.6)
            inner.circle(cx,cy,27,INK);inner.text(cx,cy-2,'SIDE A',8,GREEN,'Bold','middle');inner.text(cx,cy+10,'sinoPOP',8,PAPER,'Bold','middle')
            innerback=Art(inner.w,inner.h,PAPER);identity(innerback,13,30,INK);contacts(innerback,13,80,INK,dy=12)
            inner.svg(folder/'insert-front.svg');innerback.svg(folder/'insert-back.svg');printpdf([inner,innerback],folder/'insert-print.pdf')
        printpdf(arts,folder/'print.pdf');printpdf(arts,folder/'size-90x54-check.pdf',True)
        doc=pymupdf.open(folder/'print.pdf')
        for idx,(a,lab) in enumerate(zip(arts,['front','back'])):
            # 预览只显示成品裁切框。
            pix=doc[idx].get_pixmap(matrix=pymupdf.Matrix(6,6),clip=pymupdf.Rect(18,18,18+a.w,18+a.h),alpha=False);pix.save(folder/(lab+'-preview.png'))
            thumbs.append((name,lab,str(folder/(lab+'-preview.png'))))
        minsize=min(op[4] for a in arts for op in a.ops if op[0]=='text')
        QA.append({'direction':name,'trim_pt':[f.w,f.h],'trim_mm':[round(f.w/72*25.4,2),round(f.h/72*25.4,2)],'min_font_pt':minsize,'bleed_pt':9,'fonts_embedded':[x[3] for x in doc[1].get_fonts()],'pages':len(doc)})
    (ROOT/'qa-cards.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'card-preview-index.json').write_text(json.dumps(thumbs,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Cards built:',len(DIRS))
if __name__=='__main__':main()
