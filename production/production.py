"""SinoPOP 第二轮共享生产引擎；坐标为 pt，文字坐标为共同基线。"""
from pathlib import Path
from functools import lru_cache
from xml.sax.saxutils import escape
import base64, io, json, hashlib
from fontTools.ttLib import TTFont as FTFont
from fontTools import subset
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, CMYKColorSep, CMYKColor, Color
from reportlab.lib.utils import ImageReader
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject, ContentStream, DictionaryObject, NameObject
import pymupdf
from PIL import Image

ROOT=Path(__file__).resolve().parent
ASSET=ROOT/'assets'; FONTS=ASSET/'fonts'
INK='#111318'; SURFACE='#181A1F'; NAVY=SURFACE; PAPER='#F7F8F4'; GREEN='#73F64B'
MUTED='#B7BDC5'; SUB='#5A616C'; LINE='#3A3F48'; PALE='#D8DBD3'
PALETTE=[INK,SURFACE,PAPER,GREEN,MUTED,SUB,LINE,PALE]
MM=72/25.4
def mm(v): return float(v)*MM
FONT_NAMES=['Archivo-Regular','Archivo-Bold','Archivo-ExtraBold','NotoSansSC-Regular','NotoSansSC-Medium','NotoSansSC-Bold','NotoSansSC-Heavy']
for name in FONT_NAMES: pdfmetrics.registerFont(TTFont(name,str(FONTS/(name+'.ttf'))))
LOGOS={v:base64.b64encode((ASSET/f'sinopop-logo-{v}.svg').read_bytes()).decode() for v in ('white','black')}
DRAWINGS={v:svg2rlg(str(ASSET/f'sinopop-logo-{v}.svg')) for v in ('white','black')}
QA=[]

def remove_unused_fonts(page,reader):
    # ReportLab 会预登记基准字体；移除未真正绘制文字的资源，避免印前误报。
    current=None;stack=[];used=set()
    for args,op in ContentStream(page.get_contents(),reader).operations:
        if op==b'q':stack.append(current)
        elif op==b'Q':current=stack.pop() if stack else None
        elif op==b'Tf':current=str(args[0])
        elif op in (b'Tj',b'TJ',b"'",b'"') and current:used.add(current)
    resources=DictionaryObject(dict(page['/Resources'].get_object()));fonts=resources.get('/Font')
    if fonts:
        fonts=fonts.get_object()
        resources[NameObject('/Font')]=DictionaryObject({key:value for key,value in fonts.items() if str(key) in used})
        page[NameObject('/Resources')]=resources

def runs(s,weight='Regular'):
    arr=[]
    for ch in str(s):
        cn={'Regular':'Regular','Medium':'Medium','Bold':'Bold','ExtraBold':'Heavy','Heavy':'Heavy'}[weight]
        en={'Medium':'Regular','Heavy':'ExtraBold'}.get(weight,weight)
        font='NotoSansSC-'+cn if ord(ch)>255 else 'Archivo-'+en
        if arr and arr[-1][0]==font: arr[-1]=(font,arr[-1][1]+ch)
        else: arr.append((font,ch))
    return arr
def width(s,size,weight='Regular'):
    return sum(pdfmetrics.stringWidth(t,f,size) for f,t in runs(s,weight))

@lru_cache(maxsize=512)
def font_css(name,chars):
    f=FTFont(FONTS/(name+'.ttf')); opts=subset.Options(); opts.layout_features=['*']
    ss=subset.Subsetter(options=opts); ss.populate(text=chars); ss.subset(f)
    f.flavor='woff2'; b=io.BytesIO(); f.save(b)
    return f"@font-face{{font-family:'{name}';src:url(data:font/woff2;base64,{base64.b64encode(b.getvalue()).decode()}) format('woff2');}}"

def rgb_cmyk(rgb):
    r,g,b=rgb; k=1-max(rgb)
    return (0,0,0,1) if k>.999999 else ((1-r-k)/(1-k),(1-g-k)/(1-k),(1-b-k)/(1-k),k)

def print_color(color):
    if isinstance(color,(CMYKColor,CMYKColorSep)): return color
    if isinstance(color,str): color=HexColor(color)
    rgb=(color.red,color.green,color.blue)
    cmyk=rgb_cmyk(rgb)
    if max(abs(a-b) for a,b in zip(rgb,(115/255,246/255,75/255)))<.00001:
        return CMYKColorSep(*cmyk,spotName='SP-GREEN',density=1)
    return CMYKColor(*cmyk)

class PrintCanvas(canvas.Canvas):
    def setFillColor(self,aColor,alpha=None): super().setFillColor(print_color(aColor),alpha)
    def setStrokeColor(self,aColor,alpha=None): super().setStrokeColor(print_color(aColor),alpha)
    def setFillColorRGB(self,r,g,b,alpha=None): self.setFillColor(Color(r,g,b),alpha)
    def setStrokeColorRGB(self,r,g,b,alpha=None): self.setStrokeColor(Color(r,g,b),alpha)
    def setFillGray(self,gray,alpha=None): self.setFillColor(CMYKColor(0,0,0,1-gray),alpha)
    def setStrokeGray(self,gray,alpha=None): self.setStrokeColor(CMYKColor(0,0,0,1-gray),alpha)

class Art:
    def __init__(self,w=252,h=144,bg=SURFACE):
        self.w=w; self.h=h; self.bg=bg; self.ops=[]; self.rect(0,0,w,h,bg)
    def rect(self,x,y,w,h,c,r=0,stroke=None,sw=1): self.ops.append(('rect',x,y,w,h,c,r,stroke,sw))
    def circle(self,x,y,r,c,stroke=None,sw=1): self.ops.append(('circle',x,y,r,c,stroke,sw))
    def line(self,x,y,x2,y2,c=LINE,sw=1,dash=None): self.ops.append(('line',x,y,x2,y2,c,sw,dash))
    def poly(self,pts,c): self.ops.append(('poly',pts,c))
    def text(self,x,y,s,size=7.5,c=PAPER,weight='Regular',anchor='start',maxw=None):
        if size<7: raise ValueError(f'Font below 7 pt: {s}')
        if maxw and width(s,size,weight)>maxw+.01: raise ValueError(f'Text overflow: {s} ({width(s,size,weight)} > {maxw})')
        self.ops.append(('text',x,y,str(s),size,c,weight,anchor))
    def logo(self,x,y,w=60,v='white'): self.ops.append(('logo',x,y,w,v))
    def image(self,x,y,w,h,path): self.ops.append(('image',x,y,w,h,str(Path(path).resolve())))
    def place(self,other,x=0,y=0,scale=1,rotation=0):
        if scale!=1 or rotation:
            if rotation not in (0,180):raise ValueError('Panel rotation must be 0 or 180')
            self.ops.append(('group',other,x,y,scale,rotation));return
        for op in other.ops:
            t,*v=op
            if t in ('rect','circle','text','logo','image'): v[0]+=x; v[1]+=y
            elif t=='line': v[0]+=x;v[1]+=y;v[2]+=x;v[3]+=y
            elif t=='poly':v[0]=[(xx+x,yy+y) for xx,yy in v[0]]
            self.ops.append((t,*v))
    def all_ops(self):
        for op in self.ops:
            if op[0]=='group':yield from op[1].all_ops()
            else:yield op
    def svg(self,path=None):
        used={}
        for op in self.all_ops():
            if op[0]=='text':
                for f,t in runs(op[3],op[6]):used.setdefault(f,set()).update(t)
        css='\n'.join(font_css(f,''.join(sorted(chars))) for f,chars in sorted(used.items()))
        out=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{self.w/MM:.8f}mm" height="{self.h/MM:.8f}mm" viewBox="0 0 {self.w} {self.h}"><defs><style>{css}</style></defs>']
        for op in self.ops:
            t,*v=op
            if t=='rect':
                x,y,w,h,c,r,st,sw=v;out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{c or "none"}" stroke="{st or "none"}" stroke-width="{sw}"/>')
            elif t=='circle':
                x,y,r,c,st,sw=v;out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c or "none"}" stroke="{st or "none"}" stroke-width="{sw}"/>')
            elif t=='line':
                x,y,x2,y2,c,sw,dash=v;out.append(f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{sw}"'+(f' stroke-dasharray="{dash[0]} {dash[1]}"' if dash else '')+'/>')
            elif t=='poly':out.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in v[0])+f'" fill="{v[1]}"/>')
            elif t=='text':
                x,y,s,sz,c,we,anc=v;xx=x-(width(s,sz,we) if anc=='end' else width(s,sz,we)/2 if anc=='middle' else 0)
                for f,txt in runs(s,we):
                    out.append(f'<text x="{xx:.5f}" y="{y}" font-family="{f}" font-size="{sz}" fill="{c}" xml:space="preserve">{escape(txt)}</text>');xx+=pdfmetrics.stringWidth(txt,f,sz)
            elif t=='logo':
                x,y,w,var=v;out.append(f'<image x="{x}" y="{y}" width="{w}" height="{w*1741/2315}" preserveAspectRatio="xMidYMid meet" xlink:href="data:image/svg+xml;base64,{LOGOS[var]}"/>')
            elif t=='image':
                x,y,w,h,fp=v;data=base64.b64encode(Path(fp).read_bytes()).decode();out.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" xlink:href="data:image/png;base64,{data}"/>')
            elif t=='group':
                child,x,y,sc,rot=v;fragment=child.svg().split('</defs>',1)[1].rsplit('</svg>',1)[0]
                transform=f'translate({x+child.w*sc},{y+child.h*sc}) rotate(180) scale({sc})' if rot else f'translate({x},{y}) scale({sc})'
                out.append(f'<g transform="{transform}">{fragment}</g>')
        out.append('</svg>');result='\n'.join(out)
        if path is not None:Path(path).write_text(result,encoding='utf-8')
        return result
    def pdfdraw(self,c,ox=0,oy=0,sx=1,sy=1):
        c.saveState();c.translate(ox,oy);c.scale(sx,sy)
        for op in self.ops:
            t,*v=op
            if t=='rect':
                x,y,w,h,fill,r,st,sw=v
                if fill:c.setFillColor(HexColor(fill))
                if st:c.setStrokeColor(HexColor(st));c.setLineWidth(sw)
                c.roundRect(x,self.h-y-h,w,h,r,stroke=int(bool(st)),fill=int(bool(fill)))
            elif t=='circle':
                x,y,r,fill,st,sw=v
                if fill:c.setFillColor(HexColor(fill))
                if st:c.setStrokeColor(HexColor(st));c.setLineWidth(sw)
                c.circle(x,self.h-y,r,stroke=int(bool(st)),fill=int(bool(fill)))
            elif t=='line':
                x,y,x2,y2,col,sw,dash=v;c.setStrokeColor(HexColor(col));c.setLineWidth(sw);c.setDash(dash or []);c.line(x,self.h-y,x2,self.h-y2);c.setDash([])
            elif t=='poly':
                pts,col=v;p=c.beginPath();p.moveTo(pts[0][0],self.h-pts[0][1])
                for x,y in pts[1:]:p.lineTo(x,self.h-y)
                p.close();c.setFillColor(HexColor(col));c.drawPath(p,stroke=0,fill=1)
            elif t=='text':
                x,y,s,sz,col,we,anc=v;x-=width(s,sz,we) if anc=='end' else width(s,sz,we)/2 if anc=='middle' else 0;c.setFillColor(HexColor(col))
                for f,txt in runs(s,we):c.setFont(f,sz);c.drawString(x,self.h-y,txt);x+=pdfmetrics.stringWidth(txt,f,sz)
            elif t=='logo':
                x,y,w,var=v;d=DRAWINGS[var];c.saveState();c.translate(x,self.h-y-w*1741/2315);c.scale(w/d.width,w/d.width);renderPDF.draw(d,c,0,0);c.restoreState()
            elif t=='image':
                x,y,w,h,fp=v;im=Image.open(fp)
                if isinstance(c,PrintCanvas):im=im.convert('CMYK')
                c.drawImage(ImageReader(im),x,self.h-y-h,w,h,preserveAspectRatio=True,anchor='c',mask=None)
            elif t=='group':
                child,x,y,sc,rot=v;c.saveState()
                if rot:c.translate(x+child.w*sc,self.h-y);c.rotate(180);child.pdfdraw(c,0,0,sc,sc)
                else:child.pdfdraw(c,x,self.h-y-child.h*sc,sc,sc)
                c.restoreState()
        c.restoreState()

def printpdf(arts,path,bleed_mm=3,spot=False,technical=False):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix('.tmp.pdf')
    cls=PrintCanvas if spot else canvas.Canvas;c=cls(str(tmp),pageCompression=1,invariant=1);boxes=[]
    bleed=mm(bleed_mm);m=bleed+mm(5)
    for a in arts:
        W,H=a.w,a.h;c.setPageSize((W+2*m,H+2*m))
        c.setFillColor(HexColor(PAPER));c.rect(0,0,W+2*m,H+2*m,fill=1,stroke=0)
        if not technical:
            c.setFillColor(HexColor(a.bg));c.rect(m-bleed,m-bleed,W+2*bleed,H+2*bleed,fill=1,stroke=0)
            for op in a.ops:
                if op[0]=='rect':
                    _,x,y,w,h,fill,r,st,sw=op
                    if fill and (abs(x)<.01 or abs(y)<.01 or abs(x+w-W)<.01 or abs(y+h-H)<.01):
                        left=bleed if abs(x)<.01 else 0;right=bleed if abs(x+w-W)<.01 else 0;top=bleed if abs(y)<.01 else 0;bottom=bleed if abs(y+h-H)<.01 else 0
                        c.setFillColor(HexColor(fill));c.rect(m+x-left,m+H-y-h-bottom,w+left+right,h+top+bottom,fill=1,stroke=0)
        a.pdfdraw(c,m,m)
        c.setStrokeColor(HexColor(INK));c.setLineWidth(.25)
        gap=mm(1);ln=mm(3)
        for x in (m,m+W):c.line(x,m-bleed-gap,x,m-bleed-gap-ln);c.line(x,m+H+bleed+gap,x,m+H+bleed+gap+ln)
        for y in (m,m+H):c.line(m-bleed-gap,y,m-bleed-gap-ln,y);c.line(m+W+bleed+gap,y,m+W+bleed+gap+ln,y)
        boxes.append((W,H));c.showPage()
    c.save();reader=PdfReader(tmp);writer=PdfWriter()
    for p,(W,H) in zip(reader.pages,boxes):
        remove_unused_fonts(p,reader)
        p.trimbox=RectangleObject([m,m,m+W,m+H]);p.bleedbox=RectangleObject([m-bleed,m-bleed,m+W+bleed,m+H+bleed]);writer.add_page(p)
    writer.add_metadata({'/Title':path.stem,'/Creator':'SinoPOP production.py','/Subject':('Technical paths only' if technical else 'CMYK + SP-GREEN; printer selects fluorescent ink; no ICC proof certification' if spot else 'RGB visual proof; embedded fonts')})
    writer.write(path);tmp.unlink()

def export_art(arts,folder,stem,bleed_mm=3,preview_long=2400):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True);arts=list(arts)
    printpdf(arts,folder/(stem+'-rgb.pdf'),bleed_mm)
    printpdf(arts,folder/(stem+'-print.pdf'),bleed_mm,spot=True)
    d=pymupdf.open(folder/(stem+'-rgb.pdf'))
    meta=[]
    for i,a in enumerate(arts):
        name=stem+(f'-p{i+1:02}' if len(arts)>1 else '')
        a.svg(folder/(name+'.svg'))
        page=d[i];rect=page.trimbox;scale=preview_long/max(rect.width,rect.height);pix=page.get_pixmap(matrix=pymupdf.Matrix(scale,scale),clip=rect,alpha=False);pix.save(folder/(name+'-preview.png'))
        meta.append({'page':i+1,'width_mm':a.w/MM,'height_mm':a.h/MM,'bleed_mm':bleed_mm,'texts':[{'text':o[3],'size_pt':o[4],'weight':o[6],'x':o[1],'baseline_y':o[2]} for o in a.all_ops() if o[0]=='text']})
    (folder/(stem+'-layout.json')).write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8');d.close()

def export_technical(arts,folder,stem,bleed_mm=3):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True);arts=list(arts)
    printpdf(arts,folder/(stem+'-technical.pdf'),bleed_mm,technical=True)
    for i,a in enumerate(arts):a.svg(folder/(stem+(f'-p{i+1:02}' if len(arts)>1 else '')+'-technical.svg'))
