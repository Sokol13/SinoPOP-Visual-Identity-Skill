"""在 AI 空白底图上合成真实标志与实际字体；所有字串按同一基线绘制。"""
from pathlib import Path
import io, json, math, hashlib, shutil
from PIL import Image, ImageDraw, ImageFont
import pymupdf as fitz
from production import ROOT, ASSET, FONTS, runs, INK, SURFACE, PAPER, GREEN, MUTED, SUB, LINE
from build_credentials import pass_front, TIERS, ROLES

RAW=ROOT/'task-02-onsite'/'_raw';RAW.mkdir(parents=True,exist_ok=True)
WRAW=ROOT/'task-05-wristbands'/'_raw';WRAW.mkdir(parents=True,exist_ok=True)
S=2
RECORDS=[];CURRENT=''

def text(im,x,y,string,size,color,weight='Regular',anchor='start'):
    d=ImageDraw.Draw(im);parts=[]
    for name,part in runs(string,weight):
        f=ImageFont.truetype(str(FONTS/(name+'.ttf')),max(1,round(size*S)))
        parts.append((name,part,f,d.textlength(part,font=f)))
    full=sum(p[3] for p in parts);x*=S;y*=S
    if anchor=='middle':x-=full/2
    if anchor=='end':x-=full
    boxes=[];rr=[]
    for name,part,f,advance in parts:
        d.text((x,y),part,font=f,fill=color,anchor='ls')
        b=d.textbbox((x,y),part,font=f,anchor='ls');boxes.append(b)
        rr.append(dict(font=name,text=part,baseline=y,anchor='ls',bbox=b))
        x+=advance
    RECORDS.append(dict(file=CURRENT,text=string,weight=weight,anchor='ls',baseline=y,runs=rr,bbox=[min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes)]))

def logo(im,x,y,w,variant):
    source=ASSET/f'sinopop-logo-{variant}.svg'
    with fitz.open(stream=source.read_bytes(),filetype='svg') as d:
        p=d[0];px=p.get_pixmap(matrix=fitz.Matrix(w*S/p.rect.width,w*S/p.rect.width),alpha=True)
        art=Image.frombytes('RGBA',(px.width,px.height),px.samples)
    im.alpha_composite(art,(round(x*S),round(y*S)))

def line(im,xy,c,sw=1,dash=None):
    d=ImageDraw.Draw(im);(x1,y1),(x2,y2)=xy
    if not dash:d.line([(x1*S,y1*S),(x2*S,y2*S)],fill=c,width=max(1,round(sw*S)));return
    length=math.hypot(x2-x1,y2-y1)
    if not length:return
    pos=0
    while pos<length:
        end=min(pos+dash[0],length)
        d.line([((x1+(x2-x1)*pos/length)*S,(y1+(y2-y1)*pos/length)*S),((x1+(x2-x1)*end/length)*S,(y1+(y2-y1)*end/length)*S)],fill=c,width=max(1,round(sw*S)))
        pos+=sum(dash)

def art_on_photo(im,a,x,y,scale):
    d=ImageDraw.Draw(im)
    # 主底色由底图材质承担；其余图形按原稿等比合成，不拉伸标志或字体。
    for op in a.ops[1:]:
        t,*v=op
        if t=='text':
            xx,yy,s,sz,c,we,anc=v;text(im,x+xx*scale,y+yy*scale,s,sz*scale,c,we,anc)
        elif t=='logo':xx,yy,w,var=v;logo(im,x+xx*scale,y+yy*scale,w*scale,var)
        elif t=='rect':
            xx,yy,w,h,fill,r,stroke,sw=v;b=((x+xx*scale)*S,(y+yy*scale)*S,(x+(xx+w)*scale)*S,(y+(yy+h)*scale)*S)
            if r:d.rounded_rectangle(b,radius=r*scale*S,fill=fill,outline=stroke,width=max(1,round(sw*scale*S)))
            else:d.rectangle(b,fill=fill,outline=stroke,width=max(1,round(sw*scale*S)))
        elif t=='line':
            xx,yy,xe,ye,c,sw,dash=v;line(im,[(x+xx*scale,y+yy*scale),(x+xe*scale,y+ye*scale)],c,sw*scale,[q*scale for q in dash] if dash else None)

def wrist_mockup():
    global CURRENT
    CURRENT='task-05-wristbands/wristbands-mockup.png'
    im=Image.open(WRAW/'wristbands-blank.png').convert('RGBA').resize((3072,2048),Image.Resampling.LANCZOS)
    # 镜头仅展示手环头部，其余票面绕到手腕背面。
    for tier,lx,ly,tx,ty in [('GA',155,270,214,291),('VIP',650,270,707,291),('SVIP',1142,285,1201,307)]:
        spec=TIERS[tier];logo(im,lx,ly,49,spec['logo'])
        text(im,tx,ty,tier,30,spec['fg'],'ExtraBold')
        text(im,tx,ty+24,spec['sub'],10.5,spec['fg'],'Bold')
    im.convert('RGB').save(ROOT/CURRENT)

def kit():
    global CURRENT
    CURRENT='task-02-onsite/onsite-04-kit.png'
    im=Image.open(RAW/'onsite-04-kit-blank.png').convert('RGBA').resize((3072,2048),Image.Resampling.LANCZOS)
    d=ImageDraw.Draw(im)
    # 手环的粘扣实物位于右端，票面文本落在可印刷区内。
    for i,tier in enumerate(TIERS):
        spec=TIERS[tier];y=42+i*64
        if tier!='GA':
            # 粘扣区遵循正式票面底色，使黑档文字保持亮绿且不落在浅底上。
            d.rectangle((879*S,(y+1)*S,948*S,(y+46)*S),fill=spec['bg'])
            line(im,[(879,y+1),(879,y+46)],SUB,.5)
        logo(im,166,y+7,42,spec['logo'])
        text(im,230,y+30,tier,24,spec['fg'],'ExtraBold')
        text(im,230,y+42,spec['sub'],9,spec['fg'],'Bold')
        text(im,687,y+19,'[MM.DD] · [场地]',8,spec['fg'],'Regular')
        text(im,687,y+34,f"No. {spec['start']:06d}",8,spec['fg'],'Bold')
        text(im,914,y+20,'撕开即失效',6.5,spec['fg'],'Bold','middle')
        text(im,914,y+34,f"No. {spec['start']:06d}",6.5,spec['fg'],'Regular','middle')
    positions=[(211,348,157),(469,348,157),(737,348,155),(203,699,159),(463,697,159),(733,699,157)]
    for role,(x,y,w) in zip(ROLES,positions):
        a=pass_front(role);art_on_photo(im,a,x,y,w/a.w)
    # 选取朝向镜头的直线织带段，原始文字等比印在对应色绳上。
    # 灰绳折叠处仅露出循环印字的前段，其余自然绕到背面；不把文字印到金属扣上。
    for x,y,s,c in [(218,315,'sinoPOP · STAFF',INK),(488,311,'sinoPOP · ARTIST',GREEN),(756,311,'sinoPOP · ARTIST',GREEN),(213,665,'sinoPOP · GUEST',INK),(473,663,'sinoPOP · PRESS /',INK),(742,665,'sinoPOP · PRESS /',INK)]:
        text(im,x,y,s,5.4,c,'Bold')
    text(im,1071,154,'现场流程',28,INK,'ExtraBold')
    text(im,1423,154,'RUN OF SHOW',10,INK,'Bold','end')
    line(im,[(1071,174),(1422,174)],INK,3)
    entries=[('01','入场','DOORS'),('02','验票','CHECK-IN'),('03','寄存','COAT CHECK'),('04','酒水 · 周边','BAR · B-SIDE'),('05','演出','THE SHOW'),('06','返场 · 出口','ENCORE · WAY OUT')]
    for i,(n,cn,en) in enumerate(entries):
        yy=215+i*62;text(im,1071,yy,n,22,INK,'ExtraBold');text(im,1128,yy,cn,17,INK,'ExtraBold');text(im,1128,yy+19,en,8.5,INK,'Bold')
        text(im,1420,yy+9,'[时间]',9,SUB,'Regular','end');line(im,[(1071,yy+30),(1422,yy+30)],'#D8DBD3',.7)
    text(im,1071,613,'[艺人名] · [日期]',9,SUB,'Regular');logo(im,1377,604,42,'black')
    im.convert('RGB').save(ROOT/CURRENT)

def qa_crops():
    # 保留原始像素的逐行裁图，检查标点、连字符、小写字母和中英基线。
    q=ROOT/'_qa'/'credentials-baselines';q.mkdir(parents=True,exist_ok=True)
    pages=[];rows=[]
    for rec in RECORDS:
        assert len({r['baseline'] for r in rec['runs']})==1
        p=ROOT/rec['file'];im=Image.open(p)
        b=rec['bbox'];pad=5;crop=im.crop((max(0,math.floor(b[0])-pad),max(0,math.floor(b[1])-pad),min(im.width,math.ceil(b[2])+pad),min(im.height,math.ceil(b[3])+pad)))
        rows.append(crop)
    for start in range(0,len(rows),22):
        part=rows[start:start+22];w=max(x.width for x in part)+20;h=sum(x.height+12 for x in part)+10
        out=Image.new('RGB',(w,h),SURFACE);yy=10
        for row in part:out.paste(row,(10,yy));yy+=row.height+12
        fp=q/f'rows-{start//22+1:02}.png';out.save(fp);pages.append(str(fp.relative_to(ROOT)))
    (ROOT/'_qa'/'credentials-text-baselines.json').write_text(json.dumps(dict(anchor='ls',rows=len(RECORDS),every_run_shares_line_baseline=True,crops=pages,records=RECORDS),ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':
    wrist_mockup();kit();qa_crops()
