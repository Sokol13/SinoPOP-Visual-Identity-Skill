"""V24 黑胶封套定稿；生产展开图和刀模分开。"""
from production import *
import csv

FOLDER=ROOT/'task-04-card-final'
DEFAULT={'name_cn':'[姓名]','name_en':'[First Last]','title':'[Title · Team]','phone':'+1 [000 000 0000]','wechat':'[微信号]','email':'[name@sinopop.us]'}

def identity(a,data,x=14,y=31,c=PAPER):
    maxw=a.w-x-12
    a.text(x,y,data['name_cn'],22,c,'ExtraBold',maxw=maxw)
    a.text(x,y+15,data['name_en'],10,c,'Bold',maxw=maxw)
    a.text(x,y+29,data['title'],7.5,MUTED if c==PAPER else SUB,maxw=maxw)

def contacts(a,data,x=14,y=84,c=PAPER,dy=12):
    for i,s in enumerate([data['phone'],'WeChat '+data['wechat'],data['email'],'sinopop.us']):a.text(x,y+i*dy,s,7.5,c,maxw=a.w-x-12)

def insert(data=None):
    data=data or DEFAULT
    front=Art(mm(86.9),mm(48.8),GREEN);cx,cy=172.16535,69.16535
    for r in (59,54,49,44,39,34):front.circle(cx,cy,r,None,INK,.6)
    front.circle(cx,cy,27,INK);front.text(cx,cy-2,'SIDE A',8,GREEN,'Bold','middle');front.text(cx,cy+10,'SinoPOP',8,PAPER,'Bold','middle')
    back=Art(front.w,front.h,PAPER);identity(back,data,13,30,INK);contacts(back,data,13,80,INK)
    return front,back

def sleeve():
    front=Art();front.logo(12,11,43);front.text(14,124,'A1',32,GREEN,'ExtraBold')
    back=Art();identity(back,DEFAULT);contacts(back,DEFAULT);back.circle(236,16,7,GREEN)
    # 展开时背面在左、正面在右；中央折线成为成品左边，右边为插卡开口。
    spread=Art(mm(177.8),mm(62.8),SURFACE)
    spread.place(back,0,mm(6));spread.place(front,mm(88.9),mm(6))
    return front,back,spread

def technical():
    a=Art(mm(177.8),mm(62.8),PAPER)
    pts=[(0,6),(2,0),(86.9,0),(88.9,6),(177.8,6),(177.8,56.8),(88.9,56.8),(86.9,62.8),(2,62.8),(0,56.8)]
    for (x,y),(x2,y2) in zip(pts,pts[1:]+pts[:1]):a.line(mm(x),mm(y),mm(x2),mm(y2),INK,.5)
    for y in (6,56.8):a.line(0,mm(y),mm(88.9),mm(y),SUB,.5,(3,3))
    a.line(mm(88.9),mm(6),mm(88.9),mm(56.8),SUB,.5,(3,3))
    a.circle(mm(88.9)+175,mm(6)+72,59,None,INK,.5)
    inner=Art(mm(86.9),mm(48.8),PAPER);inner.rect(0,0,inner.w,inner.h,None,stroke=INK,sw=.5)
    return a,inner

def main():
    FOLDER.mkdir(parents=True,exist_ok=True)
    f,b,s=sleeve();export_art([s],FOLDER,'sleeve',bleed_mm=3.175)
    export_art(insert(),FOLDER,'insert',bleed_mm=3.175)
    t,it=technical();export_technical([t],FOLDER,'sleeve',bleed_mm=3.175);export_technical([it],FOLDER,'insert',bleed_mm=3.175)
    # 组合预览只用于检查露窗效果，不作为油墨版交付。
    preview=Art(mm(190),mm(68),PAPER);assembled=Art();assembled.place(f)
    assembled.circle(175,72,59,GREEN)
    for r in (54,49,44,39,34):assembled.circle(175,72,r,None,INK,.6)
    assembled.circle(175,72,27,INK);assembled.text(175,70,'SIDE A',8,GREEN,'Bold','middle');assembled.text(175,82,'SinoPOP',8,PAPER,'Bold','middle')
    preview.place(assembled,mm(5),mm(9));preview.place(insert()[1],mm(101),mm(10))
    tmp=ROOT/'_qa'/'card-assembly-rgb.pdf';printpdf([preview],tmp)
    d=pymupdf.open(tmp);pix=d[0].get_pixmap(matrix=pymupdf.Matrix(2400/preview.w,2400/preview.w),clip=d[0].trimbox);pix.save(FOLDER/'assembly-preview.png');d.close()
    with (FOLDER/'staff.csv').open('w',encoding='utf-8-sig',newline='') as fh:
        w=csv.DictWriter(fh,fieldnames=list(DEFAULT));w.writeheader();w.writerow(DEFAULT)
    print('V24 sleeve and insert built')

if __name__=='__main__':main()
