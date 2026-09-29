from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import pymupdf as fitz
import numpy as np
import cv2
import json, hashlib, io

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT.parent / 'assets'
S = 2
INK='#111318'; CHAR='#1B1E24'; PAPER='#F7F8F4'; GREEN='#73F64B'; GRAY='#B7BDC5'; RULE='#3A3F48'
FONTS={k:ASSETS/'fonts'/v for k,v in {'cn':'NotoSansSC-Heavy.ttf','cn_regular':'NotoSansSC-Regular.ttf','cn_medium':'NotoSansSC-Medium.ttf','cn_bold':'NotoSansSC-Bold.ttf','en':'Archivo-Regular.ttf','bold':'Archivo-Bold.ttf','num':'Archivo-ExtraBold.ttf'}.items()}
cache={}
TEXT_RECORDS=[]
CURRENT_FILE=''

def font(kind,size):
    key=(kind,size)
    if key not in cache: cache[key]=ImageFont.truetype(str(FONTS[kind]),round(size*S))
    return cache[key]

def cn(ch): return '\u3400' <= ch <= '\u9fff'

def text(im,xy,string,size,fill=PAPER,kind='bold',align='left'):
    # 连续语种字串一次绘制，共享字体基线；不按单字墨迹顶部对齐。
    draw=ImageDraw.Draw(im)
    runs=[]
    for c in string:
        if cn(c):
            face='cn' if size>=24 or kind=='num' else ('cn_regular' if kind=='en' else 'cn_bold')
        else:
            face=kind
        if runs and runs[-1]['face']==face:
            runs[-1]['text']+=c
        else:
            runs.append({'text':c,'face':face})
    for run in runs:
        f=font(run['face'],size)
        run['font']=FONTS[run['face']].name
        run['advance']=float(draw.textlength(run['text'],font=f))
        run['relative_bbox']=list(draw.textbbox((0,0),run['text'],font=f,anchor='ls'))
    width=sum(run['advance'] for run in runs)
    x,y=xy[0]*S,xy[1]*S
    if align=='center': x-=width/2
    elif align=='right': x-=width
    # 保持原版行顶坐标，用整行最高墨迹推导唯一基线；标点仍处于其正常字位。
    baseline=y-min(run['relative_bbox'][1] for run in runs)
    bounds=[]
    for run in runs:
        f=font(run['face'],size)
        draw.text((x,baseline),run['text'],font=f,fill=fill,anchor='ls')
        box=list(draw.textbbox((x,baseline),run['text'],font=f,anchor='ls'))
        run.update({'anchor':'ls','x':x,'baseline':baseline,'bbox':box})
        bounds.append(box)
        x+=run['advance']
    bbox=[min(b[0] for b in bounds),min(b[1] for b in bounds),max(b[2] for b in bounds),max(b[3] for b in bounds)]
    TEXT_RECORDS.append({'file':CURRENT_FILE,'text':string,'size_design_px':size,'size_render_px':round(size*S),'fill':fill,'kind':kind,'alignment':align,'anchor':'ls','baseline':baseline,'bbox':bbox,'runs':runs})

def rect(im,box,fill,outline=None,width=1,r=0):
    d=ImageDraw.Draw(im); box=tuple(round(v*S) for v in box)
    if r: d.rounded_rectangle(box,radius=r*S,fill=fill,outline=outline,width=round(width*S))
    else: d.rectangle(box,fill=fill,outline=outline,width=round(width*S))

def line(im,pts,fill,width=1):
    ImageDraw.Draw(im).line([(round(x*S),round(y*S)) for x,y in pts],fill=fill,width=round(width*S))

def ellipse(im,box,fill,outline=None,width=1):
    ImageDraw.Draw(im).ellipse(tuple(round(v*S) for v in box),fill=fill,outline=outline,width=round(width*S))

def poly(im,pts,fill): ImageDraw.Draw(im).polygon([(round(x*S),round(y*S)) for x,y in pts],fill=fill)

def arrow(im,x,y,w,color=GREEN,left=False):
    # 箭头为几何图形，避免使用系统符号字体。
    if left:
        line(im,[(x+w,y),(x,y)],color,4)
        line(im,[(x+w*.36,y-w*.30),(x,y),(x+w*.36,y+w*.30)],color,4)
    else:
        line(im,[(x,y),(x+w,y)],color,4)
        line(im,[(x+w*.64,y-w*.30),(x+w,y),(x+w*.64,y+w*.30)],color,4)

def logo(im,x,y,w,white=True):
    # 直接栅格化用户提供的原始 SVG，不重绘、改色、描边、旋转或添加效果。
    p=ASSETS/('sinopop-logo-white.svg' if white else 'sinopop-logo-black.svg')
    doc=fitz.open(stream=p.read_bytes(),filetype='svg')
    page=doc[0]; scale=w*S/page.rect.width
    pix=page.get_pixmap(matrix=fitz.Matrix(scale,scale),alpha=True)
    art=Image.frombytes('RGBA',[pix.width,pix.height],pix.samples)
    im.alpha_composite(art,(round(x*S),round(y*S)))

def base(name):
    im=Image.open(ROOT/'_raw'/name).convert('RGB')
    arr=np.array(im)
    hsv=cv2.cvtColor(arr,cv2.COLOR_RGB2HSV)
    # 照片保留绿色光和绿色材质；其余环境去色，避免暖色杂光影响品牌。
    hue=hsv[:,:,0]; keep=(hue>=34)&(hue<=87)
    hsv[:,:,1]=np.where(keep,hsv[:,:,1],0)
    arr=cv2.cvtColor(hsv,cv2.COLOR_HSV2RGB)
    return Image.fromarray(arr).resize((3072,2048),Image.Resampling.LANCZOS).convert('RGBA')

def restroom_icon(im,x,y):
    ellipse(im,(x,y,x+13,y+13),PAPER); ellipse(im,(x+30,y,x+43,y+13),PAPER)
    rect(im,(x+2,y+19,x+11,y+57),PAPER,r=3)
    line(im,[(x+2,y+54),(x+2,y+75)],PAPER,5); line(im,[(x+11,y+54),(x+11,y+75)],PAPER,5)
    line(im,[(x-3,y+22),(x-3,y+49)],PAPER,4); line(im,[(x+16,y+22),(x+16,y+49)],PAPER,4)
    poly(im,[(x+36,y+17),(x+23,y+56),(x+49,y+56)],PAPER)
    line(im,[(x+31,y+54),(x+31,y+75)],PAPER,4); line(im,[(x+42,y+54),(x+42,y+75)],PAPER,4)

def entrance():
    im=base('raw-01-entrance.png')
    logo(im,184,109,128)
    text(im,(184,251),'入场 · TRACK 01',17,GREEN)
    for label,y in [('欢迎',303),('来到',387),('现场',471)]: text(im,(180,y),label,64,PAPER)
    text(im,(184,559),'WELCOME',21,GRAY)
    text(im,(184,585),'TO THE SHOW',21,GRAY)
    text(im,(177,717),'留个纪念',21,INK)
    text(im,(177,752),'KEEP THIS STUB',10,INK)
    text(im,(177,788),'sinopop.us',22,INK)
    # 重建清晰的纸面印刷区域，保留原有纸边和顶端胶带。
    rect(im,(592,150,885,761),PAPER)
    rect(im,(592,557,885,635),GREEN)
    text(im,(614,175),'今晚的歌单',34,INK)
    text(im,(614,221),"TONIGHT'S SETLIST",14,INK)
    line(im,[(614,252),(862,252)],INK,3)
    rows=[('01','入场','DOORS',278),('02','验票','CHECK-IN',348),('03','寄存','COAT CHECK',418),('04','酒水 · 周边','BAR · B-SIDE',488),('05','演出','THE SHOW',574),('06','返场 · 出口','ENCORE · WAY OUT',675)]
    for n,zh,en,y in rows:
        text(im,(613,y),n,26,INK,'num')
        text(im,(668,y),zh,23,INK)
        text(im,(668,y+30),en,11,INK)
    text(im,(614,648),'中场 · 洗手间',12,'#5A616C')
    logo(im,831,720,42,False)
    text(im,(614,740),'[艺人名 · 日期]',10,'#5A616C')
    text(im,(1130,537),'01',98,GREEN,'num')
    logo(im,1285,541,45)
    text(im,(1140,663),'入场',51,PAPER)
    text(im,(1144,730),'DOORS ·',17,GRAY)
    text(im,(1144,752),'ENTRANCE',17,GRAY)
    arrow(im,1300,749,43)
    text(im,(1151,836),'请准备好电子票',13,GRAY)
    return im

def lobby():
    im=base('raw-02-lobby.png')
    restroom_icon(im,453,141)
    text(im,(568,104),'中场 · INTERMISSION',17,GREEN)
    text(im,(564,143),'洗手间',60,PAPER)
    text(im,(569,214),'RESTROOMS',23,PAPER)
    arrow(im,1036,169,58)
    text(im,(213,404),'03',69,INK,'num')
    logo(im,353,408,39,False)
    arrow(im,214,535,39,INK,True)
    text(im,(270,499),'寄存',46,INK)
    text(im,(269,555),'COAT CHECK',13,INK)
    line(im,[(211,618),(391,618)],'#D8DBD3',1)
    text(im,(211,646),'轻装上阵',18,INK)
    text(im,(211,676),'Travel light',13,'#5A616C','en')
    text(im,(1222,398),'06',68,GREEN,'num')
    logo(im,1372,401,43)
    text(im,(1225,481),'返场 · ENCORE',15,GREEN)
    text(im,(1223,530),'出口方向',43,PAPER)
    text(im,(1227,587),'WAY OUT',19,PAPER)
    arrow(im,1363,648,46)
    return im

def now_playing():
    im=base('raw-03-now-playing.png')
    text(im,(278,91),'正在上演',24,GREEN)
    poly(im,[(280,129),(280,143),(292,136)],GREEN)
    text(im,(301,128),'NOW PLAYING',15,GREEN)
    logo(im,552,85,55)
    text(im,(279,563),'[艺人名]',42,PAPER)
    text(im,(281,618),'[ARTIST]',15,GRAY)
    line(im,[(281,670),(603,670)],RULE,5)
    line(im,[(281,670),(398,670)],GREEN,5)
    ellipse(im,(391,662,407,678),GREEN)
    text(im,(280,693),'[时间]',12,GRAY)
    text(im,(603,693),'[日期]',12,GRAY,align='right')
    ellipse(im,(398,739,486,827),GREEN)
    poly(im,[(431,762),(431,804),(459,783)],INK)
    line(im,[(281,855),(603,855)],RULE,1)
    text(im,(282,872),'主办 · PRESENTED BY',11,GRAY)
    text(im,(603,870),'sinopop.us',14,GRAY,align='right')
    return im

def kit():
    im=base('raw-04-kit.png')
    text(im,(243,98),'普通入场 · GA',28,INK)
    text(im,(243,194),'贵宾 · VIP',28,INK)
    text(im,(243,289),'ALL ACCESS',28,GREEN)
    for x in (262,540,823): logo(im,x-39,651,78)
    text(im,(262,740),'工作人员',26,INK,align='center');text(im,(262,777),'STAFF',14,INK,align='center')
    text(im,(540,737),'艺人',30,INK,align='center');text(im,(540,777),'ARTIST',14,INK,align='center')
    text(im,(823,744),'嘉宾',31,GREEN,align='center');text(im,(823,794),'GUEST',16,GREEN,align='center')
    for x in (262,540,823):text(im,(x,868),'[姓名]',14,GRAY,align='center')
    text(im,(1030,112),'现场流程',30,INK)
    text(im,(1368,125),'RUN OF SHOW',13,INK,align='right')
    rows=[('01','入场','DOORS'),('02','验票','CHECK-IN'),('03','寄存','COAT CHECK'),('04','酒水 · 周边','BAR · B-SIDE'),('05','演出','THE SHOW'),('06','返场 · 出口','ENCORE · WAY OUT')]
    for idx,(n,zh,en) in enumerate(rows):
        y=184+idx*67
        text(im,(1028,y),n,26,INK,'num')
        text(im,(1088,y),zh,21,INK)
        text(im,(1088,y+28),en,10,INK)
        text(im,(1367,y+10),'[时间]',13,'#5A616C',align='right')
    text(im,(1030,598),'[艺人名] · [日期]',13,'#5A616C')
    logo(im,1329,582,49,False)
    return im

def photo_spot():
    im=base('raw-05-photo-spot.png')
    for cx,cy in [(350,187),(715,192),(166,345),(540,345),(349,502),(716,502)]:logo(im,cx-57,cy-43,114)
    layer=Image.new('RGBA',(400*S,300*S))
    first_layer_record=len(TEXT_RECORDS)
    text(layer,(200,20),'05',88,GREEN,'num',align='center')
    text(layer,(200,129),'站这里拍',46,PAPER,align='center')
    text(layer,(200,201),'PHOTO SPOT',23,PAPER,align='center')
    # 地面文字按实际透视压缩；原始品牌标志从不参与这一步变换。
    layer=layer.resize((round(298*S),round(91*S)),Image.Resampling.LANCZOS)
    im.alpha_composite(layer,(round(390*S),round(776*S)))
    for record in TEXT_RECORDS[first_layer_record:]:
        # 地贴源排版仍为共同基线，以下记录其最终照片坐标，便于逐行原像素验收。
        b=record['bbox']
        record['final_image_bbox']=[b[0]*298/400+390*S,b[1]*91/300+776*S,b[2]*298/400+390*S,b[3]*91/300+776*S]
        record['final_image_baseline']=record['baseline']*91/300+776*S
        record['surface']='floor_layer_before_perspective_compression'
    return im

JOBS=[('onsite-01-entrance.png','raw-01-entrance.png',entrance),('onsite-02-lobby.png','raw-02-lobby.png',lobby),('onsite-03-now-playing.png','raw-03-now-playing.png',now_playing),('onsite-04-kit.png','raw-04-kit.png',kit),('onsite-05-photo-spot.png','raw-05-photo-spot.png',photo_spot)]
records=[]
for name,raw,fn in JOBS:
    CURRENT_FILE=name
    image=fn().convert('RGB'); path=ROOT/name;image.save(path,optimize=True)
    check=Image.open(path);check.load();assert check.size==(3072,2048)
    records.append({'file':name,'raw':'_raw/'+raw,'raw_sha256':hashlib.sha256((ROOT/'_raw'/raw).read_bytes()).hexdigest(),'width':check.width,'height':check.height,'format':check.format,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'status':'existing AI raw reused, baseline-correct typography recomposited, decoded'})
    print(name,check.size)
receipt={'generation':'built-in image_gen, five independent successful calls','raw_dimensions':[1536,1024],'final_dimensions':[3072,2048],'resizing':'2x Lanczos enlargement after deterministic typography/logo composition; not native 3K generation','ai_notice':'All scene photography is AI-generated concept imagery, not records of actual sinoPOP events.','fonts':{k:p.name for k,p in FONTS.items()},'graphic_palette':[INK,CHAR,PAPER,GREEN,GRAY,RULE,'#5A616C','#D8DBD3'],'original_logo_exception':'The provided white SVG itself is #FFFFFF; retained unchanged rather than recolored. Photographic lighting, antialiasing and material tones produce continuous shades.','logo_transform':'Original SVG rendered proportionally with PyMuPDF, unrotated, unrecolored, no effects.','files':records}
receipt['generation']='Five existing built-in image_gen source files reused; no new image generation in this revision.'
receipt['typography_revision']='Contiguous language/font runs share anchor=ls baseline. Small Chinese follows Archivo Regular/Bold; large Chinese titles use Heavy.'
(ROOT/'receipt-onsite.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
# 原像素截取所有文字行，不改变输出尺寸，也不缩放验收裁片。
qa=ROOT/'_qa-baselines'
qa.mkdir(exist_ok=True)
qa_items=[]
for index,record in enumerate(TEXT_RECORDS,1):
    b=record.get('final_image_bbox',record['bbox'])
    box=(max(0,int(np.floor(b[0]))-8),max(0,int(np.floor(b[1]))-8),min(3072,int(np.ceil(b[2]))+8),min(2048,int(np.ceil(b[3]))+8))
    source=Image.open(ROOT/record['file'])
    crop=source.crop(box)
    qa_items.append((index,crop))
    record['review_crop']=list(box)
    record['all_runs_share_baseline']=len({r['baseline'] for r in record['runs']})==1
    assert record['all_runs_share_baseline']
    assert all(r['anchor']=='ls' for r in record['runs'])
for batch in range(0,len(qa_items),8):
    rows=qa_items[batch:batch+8]
    width=max(crop.width for _,crop in rows)+120
    height=sum(max(crop.height,45)+22 for _,crop in rows)+12
    sheet=Image.new('RGB',(width,height),(27,30,36))
    d=ImageDraw.Draw(sheet);y=12
    for index,crop in rows:
        d.text((10,y+3),f'{index:03d}',font=font('en',12),fill=GRAY,anchor='lt')
        sheet.paste(crop,(100,y))
        y+=max(crop.height,45)+22
    sheet.save(qa/f'lines-{batch+1:03d}-{batch+len(rows):03d}.png')
baseline_qa={'method':'Contiguous language/font runs, Pillow anchor=ls, one shared baseline per line; all crops retain 1:1 final-image pixels.','line_count':len(TEXT_RECORDS),'all_runs_share_baseline':all(r['all_runs_share_baseline'] for r in TEXT_RECORDS),'visual_review':'pending','records':TEXT_RECORDS}
(ROOT/'baseline-qa.json').write_text(json.dumps(baseline_qa,ensure_ascii=False,indent=2),encoding='utf-8')
