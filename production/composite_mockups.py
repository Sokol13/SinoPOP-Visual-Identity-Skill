from pathlib import Path
import io, json, copy
import numpy as np
import cv2
from PIL import Image, ImageOps, ImageDraw
import pymupdf
from reportlab.pdfgen import canvas
import build_cards as b

ROOT=Path(__file__).resolve().parent
BASE=ROOT/'task-01-cards'
records=[]
def render(a, remove_bg=True, filt=None, scale=8):
    t=copy.copy(a); t.ops=a.ops[1:] if remove_bg else list(a.ops)
    if filt: t.ops=[op for op in t.ops if filt(op)]
    bio=io.BytesIO(); c=canvas.Canvas(bio,pagesize=(a.w,a.h),pageCompression=1)
    t.pdfdraw(c); c.showPage(); c.save()
    d=pymupdf.open(stream=bio.getvalue(),filetype='pdf')
    p=d[0].get_pixmap(matrix=pymupdf.Matrix(scale,scale),alpha=True)
    # MuPDF 返回预乘 alpha，先解除预乘再合成，避免深边。
    x=np.frombuffer(p.samples,np.uint8).reshape(p.height,p.width,4).copy().astype(np.float32)
    al=x[:,:,3:4]/255
    x[:,:,:3]=np.where(al>0,x[:,:,:3]/np.maximum(al,.001),0)
    return np.clip(x,0,255).astype(np.uint8)

def warp(layer,quad,shape):
    h,w=layer.shape[:2]
    src=np.float32([[0,0],[w,0],[w,h],[0,h]])
    H=cv2.getPerspectiveTransform(src,np.float32(quad))
    return cv2.warpPerspective(layer,H,(shape[1],shape[0]),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT)

def place(im,layer,quad,light=1.0):
    ov=warp(layer,quad,im.shape).astype(np.float32)
    alpha=np.clip(ov[:,:,3:4]/255,0,1)
    # 保留图层透明处的原摄影材质；油墨层只施加轻微统一光照。
    im[:]=np.clip(ov[:,:,:3]*light*alpha+im*(1-alpha),0,255)
    return im

def blank_green(im,quad,inpaint=False):
    mask=np.zeros(im.shape[:2],np.uint8);cv2.fillConvexPoly(mask,np.int32(quad),255)
    pix=im.astype(np.float32)
    green=(pix[:,:,1]>pix[:,:,0]*1.30)&(pix[:,:,1]>pix[:,:,2]*1.30)&(pix[:,:,1]>60)&(mask>0)
    if inpaint:
        mask=green.astype(np.uint8)*255
        mask=cv2.dilate(mask,np.ones((5,5),np.uint8))
        return cv2.inpaint(im,mask,5,cv2.INPAINT_TELEA)
    shade=np.clip(pix[:,:,1]/185,.55,1.4)
    for j,v in enumerate([17,19,24]): im[:,:,j]=np.where(green,v*shade,im[:,:,j]).astype(np.uint8)
    return im

def save(name,im,notes):
    path=BASE/name/'mockup.png'
    Image.fromarray(im).resize((2400,1800),Image.Resampling.LANCZOS).save(path,optimize=True)
    with Image.open(path) as check: check.load(); size=check.size
    records.append({'folder':name,'final':'task-01-cards/'+name+'/mockup.png','dimensions':list(size),'source':'mockup-raw.png','method':'Real embedded font and original-SVG vector artwork rasterized at 8x, transparent ink overlays; physical-plane perspective compositing; Lanczos 1448x1086 to 2400x1800.','notes':notes})

def load(name): return np.array(Image.open(BASE/name/'mockup-raw.png').convert('RGB')).copy()

def direct_logo(im,x,y,w):
    # 近正面卡片单独等比放置原标志，避免底图物件比例误差使标志变形。
    h=w*1741/2315
    a=b.Art(100,100*1741/2315);a.ops=[];a.logo(0,0,100)
    place(im,render(a,remove_bg=False),[[x,y],[x+w,y],[x+w,y+h],[x,y+h]],.96)

# 01 票根左右纸面分别合成，避开半圆缺口及撕裂边。
name='01-ticket';im=load(name);f,_=b.ticket()
lay=render(f,filt=lambda op: not(op[0] in ['circle','logo'] or (op[0]=='rect' and op[1]==168)))
place(im,lay[:,:168*8],[[240,294],[972,294],[980,758],[237,757]],.96)
place(im,lay[:,168*8:],[[979,295],[1207,258],[1222,728],[984,755]],.92)
direct_logo(im,306,352,252)
save(name,im,'Front artwork split at the perforation; transparent logo and number on black paper, exact ADMIT ONE and serial on green stub. Generated tear retained; original SVG logo source unchanged.')

# 02 歌单保留纸、印刷胶带及横线，文字使用原正面排版。
name='02-setlist';im=load(name);f,_=b.setlist()
lay=render(f,filt=lambda op:op[0] not in ['poly'] and not(op[0]=='line' and op[2]==24))
place(im,lay,[[368,268],[1077,268],[1094,712],[348,712]],.97)
save(name,im,'Setlist front typography only; paper and green tape stay photographic. This photographed side intentionally has no logo, matching front.svg; back.svg carries original black-ground white logo.')

# 03 封套只加原标志、编号、真实标签字；内卡展示姓名与全部联系方式。
name='03-vinyl';im=load(name)
sl=b.Art(252,144);sl.ops=[];sl.text(16,131,'03',27,b.GREEN,'ExtraBold')
place(im,render(sl,remove_bg=False),[[550,219],[1317,219],[1317,793],[545,793]],.94)
direct_logo(im,594,279,174)
lab=b.Art(90,74);lab.ops=[];lab.text(45,29,'SIDE A',9,b.INK,'Bold','middle');lab.text(45,47,'sinoPOP',9,b.INK,'Bold','middle')
place(im,render(lab,remove_bg=False),[[946,445],[1112,445],[1112,580],[946,580]],.9)
inner=b.Art(144,204,b.PAPER);inner.ops=[]
inner.text(11,34,'[姓名]',22,b.INK,'ExtraBold');inner.text(11,51,'First Last',10,b.INK,'Bold');inner.text(11,68,'Title · Team',7.5,b.SUB)
for i,s in enumerate(['+1 [000 000 0000]','WeChat [微信号]','name@sinopop.us','sinopop.us']):inner.text(11,111+i*22,s,8,b.INK)
place(im,render(inner,remove_bg=False),[[148,226],[535,226],[531,773],[144,770]],.95)
save(name,im,'Original sleeve logo and 03 added outside the die-cut. SIDE A/sinoPOP uses Archivo on existing blank center label. Visible pull-out portion is adapted to a tall exposure with all placeholder details in true fonts; wood/light are conceptual photographic materials.')

# 04 三张后台证复用同一正面稿；先去除生图色带，再安放原稿准确色带。
name='04-backstage';im=load(name);f,_=b.backstage()
quads=[[[325,321],[530,334],[489,780],[289,740]],[[549,314],[874,314],[878,882],[547,882]],[[910,376],[1132,348],[1164,772],[942,812]]]
for q in quads: im=blank_green(im,q)
lay=render(f,filt=lambda op:not(op[0]=='rect' and op[1]==55))
for q in quads: place(im,lay,q,.94)
save(name,im,'Three true front artworks applied to the three card planes. Generated middle bands neutralized and replaced at the source-layout position. Existing punched slots, metal clips and green lanyards retained. Source logos remain original artwork, seen in physical perspective.')

# 05 透明磁带盒保留高光，封面映射原稿；打开的内页映射联系方式。
name='05-jcard';im=load(name);f,back=b.jcard()
q=[[202,510],[817,626],[780,981],[93,848]]
im=blank_green(im,q,inpaint=True)
place(im,render(f),q,.96)
place(im,render(back),[[642,121],[888,180],[844,569],[525,497]],.96)
save(name,im,'Closed cassette case receives exact cover artwork, with original logo and source green rule. Existing generated lower green rule removed locally. Open case receives true-font inside contact artwork; transparent hinges and highlights retained.')

# 06 仅油墨/压凹参考层合成，纸纤维和十张绿色刷边保持摄影底图。
name='06-material';im=load(name);f,_=b.material()
place(im,render(f),[[109,318],[1124,152],[1384,480],[281,692]],.88)
save(name,im,'Top card front true artwork applied transparently; dark-gray name is a restrained flat deboss position simulation, without fake bevel or added glow. White logo original SVG. Generated cotton fibers and green painted stack edges retained.')

p=ROOT/'receipt-mockups.json'
data=json.loads(p.read_text(encoding='utf-8'));data['final_composites']=records;data['final_status']='Six final 2400x1800 PNGs created and decoded; contact-sheet visual QA pending.'
p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
# 合成检查图只用于检查，不替代单张 2400px 交付。
sheet=Image.new('RGB',(1440,810),(17,19,24))
for i,rec in enumerate(records):
    image=Image.open(ROOT/rec['final']).convert('RGB').resize((480,360),Image.Resampling.LANCZOS)
    x=(i%3)*480;y=(i//3)*405
    sheet.paste(image,(x,y))
    ImageDraw.Draw(sheet).text((x+12,y+374),rec['folder'],fill=(247,248,244))
sheet.save(ROOT/'mockups-contact-sheet.jpg',quality=93)
print(json.dumps(records,ensure_ascii=False,indent=2))


