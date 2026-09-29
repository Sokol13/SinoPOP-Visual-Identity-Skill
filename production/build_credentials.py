"""生成手环、工牌、挂绳；所有文字坐标均采用共同基线。"""
from pathlib import Path
import csv, json, argparse
from production import Art, mm, width, export_art, export_technical, ROOT, INK, SURFACE, PAPER, GREEN, MUTED, SUB, LINE, PALE

W_DIR=ROOT/'task-05-wristbands'
P_DIR=ROOT/'task-06-passes-lanyards'
TIERS={
    'GA': dict(bg=PAPER,fg=INK,logo='black',sub='普通入场 · 早鸟同档',start=1),
    'VIP':dict(bg=GREEN,fg=INK,logo='black',sub='贵宾',start=100001),
    'SVIP':dict(bg=INK,fg=GREEN,logo='white',sub='至尊 · 卡座',start=200001),
}
ROLES={
    'STAFF':dict(cn='主办团队',band=GREEN,fg=INK,zones='1,2,3,4',lanyard='staff'),
    'ARTIST':dict(cn='艺人',band=INK,fg=GREEN,border=GREEN,sw=3,zones='1,2,3,4',lanyard='artist'),
    'ARTIST TEAM':dict(cn='艺人团队',band=INK,fg=PAPER,border=GREEN,sw=1,zones='1,2,3,4',lanyard='artist'),
    'GUEST':dict(cn='嘉宾',band=PAPER,fg=INK,zones='1,2?',lanyard='guest'),
    'PRESS':dict(cn='媒体',band=MUTED,fg=INK,zones='1',lanyard='press-production'),
    'PRODUCTION':dict(cn='制作',band=INK,fg=MUTED,border=MUTED,sw=1,zones='1,2,3',lanyard='press-production'),
}
LANYARDS={
    'staff':(GREEN,INK,'SinoPOP · STAFF'),
    'artist':(INK,GREEN,'SinoPOP · ARTIST'),
    'guest':(PAPER,INK,'SinoPOP · GUEST'),
    'press-production':(MUTED,INK,'SinoPOP · PRESS / PRODUCTION'),
}

def wristband(tier='GA',serial=1):
    spec=TIERS[tier];a=Art(mm(250),mm(25),spec['bg']);fg=spec['fg']
    a.logo(mm(5),mm(3.8),mm(23),spec['logo'])
    a.text(mm(35),mm(13.8),tier,31,fg,'ExtraBold')
    a.text(mm(35),mm(20.3),spec['sub'],9.5,fg,'Bold')
    a.text(mm(161),mm(10.2),'[MM.DD] · [场地]',8.5,fg,'Regular',maxw=mm(48))
    a.text(mm(161),mm(17.4),f'No. {serial:06d}',8.5,fg,'Bold')
    a.text(mm(231),mm(10.8),'撕开即失效',7.5,fg,'Bold','middle')
    a.text(mm(231),mm(17.1),f'No. {serial:06d}',7,fg,'Regular','middle')
    return a

def wrist_technical():
    a=Art(mm(250),mm(25),PAPER)
    a.rect(0,0,a.w,a.h,None,stroke=INK,sw=.5)
    a.line(mm(212),0,mm(212),mm(25),INK,.5,(mm(1),mm(1)))
    a.text(mm(5),mm(13),'成品 250 × 25 mm · 实线裁切 / 虚线为粘扣区边界',7,INK,'Regular')
    a.text(mm(231),mm(13),'粘扣区 38 mm',7,INK,'Bold','middle')
    return a

def zone_states(role,zones=None):
    value=ROLES[role]['zones'] if zones is None or not zones.strip() else zones.strip()
    out={i:'denied' for i in range(1,5)}
    for item in value.replace(';',',').split(','):
        item=item.strip()
        if not item: continue
        invited=item.endswith('?');raw=item[:-1] if invited else item
        if raw not in ('1','2','3','4'): raise ValueError('zones 只接受 1–4，以逗号分隔；数字后 ? 表示按邀请开放')
        if out[int(raw)]!='denied': raise ValueError('zones 内区域重复')
        out[int(raw)]='invited' if invited else 'allowed'
    return out

def pass_front(role='STAFF',name='[姓名]',zones=None):
    spec=ROLES[role];a=Art(mm(90),mm(130),SURFACE)
    a.logo(mm(9),mm(14),mm(29),'white')
    a.rect(0,mm(47),mm(90),mm(29),spec['band'])
    if 'border' in spec:
        sw=spec['sw'];a.rect(sw/2,mm(47)+sw/2,mm(90)-sw,mm(29)-sw,None,stroke=spec['border'],sw=sw)
    a.text(mm(8),mm(60),spec['cn'],21,spec['fg'],'ExtraBold',maxw=mm(74))
    a.text(mm(8),mm(69.7),role,11.5,spec['fg'],'Bold')
    size=20
    while width(name,size,'ExtraBold')>mm(74) and size>9:size-=.5
    a.text(mm(8),mm(94),name,size,PAPER,'ExtraBold',maxw=mm(74))
    states=zone_states(role,zones)
    for i in range(1,5):
        x=mm(8+(i-1)*19);y=mm(108);w=mm(14)
        if states[i]=='allowed':a.rect(x,y,w,w,PAPER,r=mm(1.3));fg=INK
        elif states[i]=='invited':
            for xa,ya,xb,yb in [(x,y,x+w,y),(x+w,y,x+w,y+w),(x+w,y+w,x,y+w),(x,y+w,x,y)]:a.line(xa,ya,xb,yb,MUTED,.7,(mm(.8),mm(.6)))
            fg=MUTED
        else:a.rect(x,y,w,w,None,r=mm(1.3),stroke=LINE,sw=.6);fg=LINE
        a.text(x+w/2,y+mm(9.7),str(i),17,fg,'ExtraBold','middle')
    return a

def pass_back():
    a=Art(mm(90),mm(130),SURFACE);a.logo(mm(9),mm(14),mm(27),'white')
    a.text(mm(8),mm(49),'通行区域',18,PAPER,'ExtraBold');a.text(mm(8),mm(57),'ACCESS ZONES',8.5,MUTED,'Bold')
    legends=[('场内','FLOOR'),('后台','BACKSTAGE'),('舞台','STAGE'),('艺人休息室','GREEN ROOM')]
    for i,(cn,en) in enumerate(legends,1):
        y=mm(66+(i-1)*10);a.rect(mm(8),y,mm(6),mm(6),PAPER,r=mm(.8));a.text(mm(11),y+mm(4.4),str(i),9,INK,'Bold','middle')
        a.text(mm(18),y+mm(4.4),cn+' '+en,8.5,PAPER,'Regular',maxw=mm(65))
    a.line(mm(8),mm(106),mm(82),mm(106),LINE,.5)
    a.text(mm(8),mm(113),'白格 = 可进入 · 空格 = 不可进入',7,MUTED,'Regular')
    a.text(mm(8),mm(119),'虚线格 = 按邀请开放',7,MUTED,'Regular')
    a.text(mm(82),mm(125),'sinopop.us',7,PAPER,'Bold','end')
    return a

def pass_technical():
    a=Art(mm(90),mm(130),PAPER);a.rect(0,0,a.w,a.h,None,r=mm(2.1),stroke=INK,sw=.5)
    a.rect(mm(38),mm(6),mm(14),mm(3),None,r=mm(1.5),stroke=INK,sw=.5)
    a.text(mm(9),mm(43),'工牌 90 × 130 mm',9,INK,'Bold')
    for i,s in enumerate(['实线：外轮廓模切及挂孔','圆角 R 2.1 mm','挂孔 14 × 3 mm · 距顶 6 mm','刀模与印刷面套准，正反同向','孔位及圆角在批量制作前确认']):a.text(mm(9),mm(55+i*9),s,7.5,INK,'Regular')
    return a

def lanyard(kind='staff'):
    bg,fg,label=LANYARDS[kind];a=Art(mm(900),mm(20),bg)
    step=110 if kind=='press-production' else 88
    for x in range(18,870,step):
        if mm(x)+width(label,13,'Bold')<mm(885):a.text(mm(x),mm(12),label,13,fg,'Bold')
    return a

def lanyard_technical():
    a=Art(mm(900),mm(20),PAPER);a.rect(0,0,a.w,a.h,None,stroke=INK,sw=.5)
    for x in (15,885):a.line(mm(x),0,mm(x),mm(20),INK,.5,(mm(1),mm(1)))
    a.text(mm(30),mm(12),'展开 900 × 20 mm · 双面同向循环印字 · 两端 15 mm 为装配预留（折返及扣件由加工厂确认）',9,INK,'Regular')
    return a

def impose_wristbands(tier,count,start):
    if count<1:raise ValueError('数量必须大于 0')
    if start<1 or start+count-1>999999:raise ValueError('流水号必须为 1–999999')
    sheets=[];tech=[]
    # A3 纸面上每条保留独立 3 mm 出血，条与条之间净间距为 8 mm。
    for offset in range(0,count,11):
        a=Art(mm(297),mm(420),PAPER);t=Art(mm(297),mm(420),PAPER)
        for j in range(min(11,count-offset)):
            x=23.5;y=18+j*34
            a.rect(mm(x-3),mm(y-3),mm(256),mm(31),TIERS[tier]['bg'])
            a.place(wristband(tier,start+offset+j),mm(x),mm(y))
            for xx in (x,x+250):
                a.line(mm(xx),mm(y-4),mm(xx),mm(y-5.5),INK,.25);a.line(mm(xx),mm(y+29),mm(xx),mm(y+30.5),INK,.25)
            for yy in (y,y+25):
                a.line(mm(x-4),mm(yy),mm(x-5.5),mm(yy),INK,.25);a.line(mm(x+254),mm(yy),mm(x+255.5),mm(yy),INK,.25)
            t.rect(mm(x),mm(y),mm(250),mm(25),None,stroke=INK,sw=.4)
            t.line(mm(x+212),mm(y),mm(x+212),mm(y+25),INK,.4,(mm(1),mm(1)))
        sheets.append(a);tech.append(t)
    return sheets,tech

def batch_wristbands(counts,starts,output):
    output=Path(output);ranges=[];summary=[]
    # 先检查整份任务，避免无效号段留下半套生产文件。
    for tier in TIERS:
        n=counts.get(tier,0)
        if n<0:raise ValueError('数量不可为负')
        if not n:continue
        start=starts.get(tier,TIERS[tier]['start']);end=start+n-1
        if start<1 or end>999999:raise ValueError('流水号必须为 1–999999')
        if any(start<=hi and end>=lo for lo,hi in ranges):raise ValueError('各票档流水号段不可重叠')
        ranges.append((start,end))
    output.mkdir(parents=True,exist_ok=True)
    for tier in TIERS:
        n=counts.get(tier,0)
        if not n:continue
        start=starts.get(tier,TIERS[tier]['start']);end=start+n-1
        arts,tech=impose_wristbands(tier,n,start)
        export_art(arts,output,tier.lower()+'-imposed',3)
        export_technical(tech,output,tier.lower()+'-imposed',3)
        summary.append(dict(tier=tier,count=n,start=start,end=end,sheets=len(arts),sheet_mm=[297,420],items_per_sheet=11))
    (output/'serial-ranges.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')

def batch_passes(csv_path,output):
    output=Path(output);summary=[];prepared=[]
    with open(csv_path,encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f)
        if reader.fieldnames!=['name','role','zones']:raise ValueError('CSV 列必须为 name,role,zones')
        rows=list(reader)
    if not rows:raise ValueError('CSV 至少需要一条人员记录')
    # 整份输入及文字适配全部验证通过后才创建目录、写出文件，防止误用半套输出。
    for i,row in enumerate(rows,1):
        try:
            if None in row or any(row.get(k) is None for k in ('name','role','zones')):raise ValueError('每行必须恰有 name,role,zones 三列')
            role=row['role'].strip().upper()
            if role not in ROLES:raise ValueError('不支持的角色: '+role)
            name=row['name'].strip()
            if not name:raise ValueError('name 不能为空')
            stem=f'pass-{i:04d}-'+role.lower().replace(' ','-')
            states=zone_states(role,row['zones'])
            arts=[pass_front(role,name,row['zones']),pass_back()]
            prepared.append((stem,arts))
            summary.append(dict(file=stem,role=role,name=name,zones=states))
        except ValueError as exc:
            raise ValueError(f'CSV 第 {i+1} 行：{exc}') from exc
    output.mkdir(parents=True,exist_ok=True)
    for stem,arts in prepared:export_art(arts,output,stem,3)
    (output/'batch-index.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')

def main():
    W_DIR.mkdir(exist_ok=True);P_DIR.mkdir(exist_ok=True)
    for tier,spec in TIERS.items():export_art([wristband(tier,spec['start'])],W_DIR,'wristband-'+tier.lower(),3)
    export_technical([wrist_technical()],W_DIR,'wristband',3)
    for role in ROLES:export_art([pass_front(role),pass_back()],P_DIR,'pass-'+role.lower().replace(' ','-'),3)
    export_technical([pass_technical()],P_DIR,'pass',3)
    for kind in LANYARDS:export_art([lanyard(kind),lanyard(kind)],P_DIR,'lanyard-'+kind,3,preview_long=5400)
    export_technical([lanyard_technical()],P_DIR,'lanyard',3)
    batch_wristbands({'GA':2,'VIP':2,'SVIP':2},{k:s['start'] for k,s in TIERS.items()},W_DIR/'batch-example')
    with (P_DIR/'passes.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['name','role','zones'])
        for role,spec in ROLES.items():w.writerow(['[姓名]',role,spec['zones']])
    with (W_DIR/'quantities.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['tier','quantity','start_serial']);w.writerows([(k,2,s['start']) for k,s in TIERS.items()])
    batch_passes(P_DIR/'passes.csv',P_DIR/'batch-example')

if __name__=='__main__':main()
