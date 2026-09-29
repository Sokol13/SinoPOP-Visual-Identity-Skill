from build_cards import *

def move_ops(a,b,dx,dy):
    for op in a.ops:
        t,*v=op
        if t in ['rect','circle','text','logo']:v[0]+=dx;v[1]+=dy
        elif t=='line':v[0]+=dx;v[1]+=dy;v[2]+=dx;v[3]+=dy
        elif t=='poly':v[0]=[(x+dx,y+dy) for x,y in v[0]]
        b.ops.append((t,*v))

def technical():
    pages=[]
    for idx,name in enumerate(DIRS):
        a=Art(540,432,PAPER)
        a.text(24,32,f'{idx+1:02} / '+name.split('-',1)[1].upper(),19,INK,'ExtraBold')
        a.text(24,50,'CONSTRUCTION GUIDE  /  NOT AN INK LAYER',8,SUB,'Bold')
        if idx==0:
            a.rect(40,90,252,144,None,0,INK,.8);a.line(208,90,208,234,INK,.6,(3,3));a.circle(208,90,6,None,INK,.7);a.circle(208,234,6,None,INK,.7)
            lines=['Trim: 88.9 x 50.8 mm (3.5 x 2 in).','Perforation: x = 59.27 mm from left.','Notches: radius 2.12 mm, centered on tear line.','Print both faces before perforation.','The barcode-like stripes are decorative, not scannable.']
        elif idx==1:
            a.rect(40,90,252,144,None,0,INK,.8)
            a.poly([(113,90),(221,90),(218,97),(221,101),(218,106),(115,104),(117,100),(113,96)],GREEN)
            lines=['Trim: 88.9 x 50.8 mm.','Torn tape is printed artwork, not an adhesive layer.','Uncoated paper; two-sided ink printing.','No special cutting is required.','Keep the 7 pt labels at original print size.']
        elif idx==2:
            # 封套是双面折片，右边留开口；胶翼只位于顶端和底端。
            a.rect(24,91,504,144,None,0,INK,.8);a.line(276,91,276,235,INK,.7,(3,3))
            a.rect(276,74,252,17,PALE,stroke=INK,sw=.7);a.rect(276,235,252,17,PALE,stroke=INK,sw=.7)
            a.circle(199,163,59,None,INK,.8);a.text(150,170,'WINDOW',8,INK,'Bold')
            a.text(326,86,'GLUE FLAP / 6 mm',7,INK,'Bold');a.text(326,247,'GLUE FLAP / 6 mm',7,INK,'Bold')
            lines=['Sleeve panel: 88.9 x 50.8 mm; opening on right.','Window: diameter 41.63 mm; center (61.74, 25.4) mm.','Pocket uses two 6 mm glue flaps and one fold.','Suggested insert trim: 86.9 x 48.8 mm; test the fit.','Use insert-print.pdf for the separate inner card.']
        elif idx==3:
            a.rect(40,82,144,252,None,6,INK,.8);a.rect(95,93,34,5,None,2.5,INK,.8)
            lines=['Trim: 50.8 x 88.9 mm; corner radius 2.12 mm.','Slot: 12.0 x 1.76 mm, 3.88 mm from top.','Slot and rounded corners are die cut, not printed.','The green band is flat ink; lanyard is separate.']
        elif idx==4:
            a.rect(36,98,396,144,None,0,INK,.8);a.line(144,98,144,242,INK,.7,(3,3));a.line(180,98,180,242,INK,.7,(3,3))
            a.text(48,263,'38.1 mm',8,INK);a.text(145,284,'12.7',8,INK);a.text(251,263,'88.9 mm',8,INK)
            lines=['Open trim: 139.7 x 50.8 mm; closed face: 88.9 x 50.8 mm.','Outer panel order: rear flap / spine / front cover.','Inside sheet is mirrored for two-sided registration.','Score before folding; confirm paper caliper with printer.','Mini business-card insert; not a standard full-size cassette J-card.']
        else:
            a.rect(40,105,252,144,INK);a.text(56,171,'[姓名]',29,LINE,'ExtraBold');a.line(40,252,292,252,GREEN,3)
            lines=['Material intent: 600 gsm black cotton, green painted edges.','Name and First Last: blind deboss from separate mask.','No green gradient or printed fake depth.','Back copy and original white logo use opaque white ink.','Confirm stock caliper, deboss depth and edge-paint sample.']
        start=354 if idx==3 else 300
        for j,s in enumerate(lines):a.text(24,start+j*15,s,8,INK)
        folder=ROOT/'task-01-cards'/name;a.svg(folder/'construction-guide.svg');pages.append(a)
    printpdf(pages,ROOT/'task-01-cards'/'construction-guides.pdf')
    # 压凹版为单独的纯黑形状与文字，不混进白墨版。
    mask=Art(bg=PAPER);mask.text(17,68,'[姓名]',29,INK,'ExtraBold');mask.text(18,87,'First Last',10,INK,'Bold');mask.svg(ROOT/'task-01-cards'/'06-material'/'deboss-mask.svg');printpdf([mask],ROOT/'task-01-cards'/'06-material'/'deboss-mask.pdf')
    ink=Art();ink.logo(199,16,36);ink.line(18,121,233,121,GREEN,1);ink.svg(ROOT/'task-01-cards'/'06-material'/'front-ink.svg');printpdf([ink,material()[1]],ROOT/'task-01-cards'/'06-material'/'ink-print.pdf')
    # 抽卡的正反面缩进 1mm 裁切；图案仍与封套圆窗中心对齐。
    ins=Art(246.3307,138.3307,GREEN);cx,cy=172.16535,69.16535
    for r in [59,54,49,44,39,34]:ins.circle(cx,cy,r,None,INK,.6)
    ins.circle(cx,cy,27,INK);ins.text(cx,cy-2,'SIDE A',8,GREEN,'Bold','middle');ins.text(cx,cy+10,'sinoPOP',8,PAPER,'Bold','middle')
    back=Art(ins.w,ins.h,PAPER);identity(back,13,30,INK);contacts(back,13,80,INK,dy=12)
    p=ROOT/'task-01-cards'/'03-vinyl';ins.svg(p/'insert-front.svg');back.svg(p/'insert-back.svg');printpdf([ins,back],p/'insert-print.pdf')
    # 窗内不印绿色唱片；由抽卡透过模切圆窗呈现。
    shell=Art();shell.logo(12,11,43);shell.text(14,124,'03',32,GREEN,'ExtraBold');shell.svg(p/'sleeve-front-ink.svg');printpdf([shell,vinyl()[1]],p/'sleeve-ink-print.pdf')
    print('Technical guides built')
if __name__=='__main__':technical()

