"""工牌套装 2.2：PVC 工牌（正反面）、场次贴、挂绳、技术图与批量输出。坐标单位 pt，文字为共同基线。

python build_badges.py                                   # 重新生成 task-10-badge-kit 全部样稿
python build_badges.py --batch people.csv --output DIR   # 按名单批量出工牌（一份多页 PDF）
"""
from pathlib import Path
import csv, json, argparse
from production import Art, mm, width, export_art, export_technical, ROOT, INK, SURFACE, PAPER, GREEN, MUTED, SUB, LINE, PALE
from build_credentials import ROLES, zone_states

OUT = ROOT/'task-10-badge-kit'
W, H = mm(90), mm(130)
ZONES = [('场内', 'FLOOR'), ('后台', 'BACKSTAGE'), ('舞台', 'STAGE'), ('休息室', 'GREEN ROOM')]
# 挂绳：织带色、印色、标志版本、中文身份
LANYARDS = {
    'staff': dict(bg=GREEN, fg=INK, logo='black', en='STAFF', cn='主办团队'),
    'artist': dict(bg=INK, fg=GREEN, logo='white', en='ARTIST', cn='艺人'),
    'guest': dict(bg=PAPER, fg=INK, logo='black', en='GUEST', cn='嘉宾'),
    'press-production': dict(bg=MUTED, fg=INK, logo='black', en='PRESS / PRODUCTION', cn='媒体 · 制作'),
}
STICKERS = {'odd': (GREEN, INK), 'even': (PAPER, INK)}  # 单数场绿、双数场白，相邻两场一眼可分


def fit(s, size, weight, maxw, floor=9):
    while width(s, size, weight) > maxw and size > floor: size -= .5
    return size


def zone_boxes(a, states, y, fg_on=INK):
    """四个通行格 + 下方中文标签。白格=可进入，虚线=按邀请，空格=不可进入。"""
    for i in range(1, 5):
        x = mm(8 + (i-1)*20); w = mm(14); st = states[i]
        if st == 'allowed': a.rect(x, y, w, w, PAPER, r=mm(1.3)); c = fg_on; lc = PAPER
        elif st == 'invited':
            for xa, ya, xb, yb in [(x, y, x+w, y), (x+w, y, x+w, y+w), (x+w, y+w, x, y+w), (x, y+w, x, y)]:
                a.line(xa, ya, xb, yb, MUTED, .7, (mm(.8), mm(.6)))
            c = MUTED; lc = MUTED
        else: a.rect(x, y, w, w, None, r=mm(1.3), stroke=LINE, sw=.6); c = LINE; lc = SUB
        a.text(x+w/2, y+mm(9.7), str(i), 17, c, 'ExtraBold', 'middle')
        a.text(x+w/2, y+w+mm(4), ZONES[i-1][0], 7, lc, 'Medium', 'middle')


def front(role='STAFF', name='[姓名]', zones=None, serial=1, title=''):
    spec = ROLES[role]; a = Art(W, H, SURFACE)
    # 头部：标志 + 场次贴位（像黑胶标签，按场贴，防止旧证复用）
    a.logo(mm(8), mm(14), mm(26), 'white')
    a.circle(mm(73), mm(23), mm(9), None, stroke=LINE, sw=.6)
    a.text(mm(73), mm(22.4), '场次贴', 7, SUB, 'Medium', 'middle')
    a.text(mm(73), mm(26.6), 'SHOW', 7, SUB, 'Bold', 'middle')
    # 身份色块：中文身份最大，英文次之
    a.rect(0, mm(40), W, mm(42), spec['band'])
    if 'border' in spec:
        sw = spec['sw']; a.rect(sw/2, mm(40)+sw/2, W-sw, mm(42)-sw, None, stroke=spec['border'], sw=sw)
    a.text(mm(8), mm(47.5), '通行证 PASS', 7, spec['fg'], 'Bold')
    a.text(mm(8), mm(67), spec['cn'], 40, spec['fg'], 'Heavy', maxw=mm(74))
    a.text(mm(8), mm(76.5), role, 14, spec['fg'], 'ExtraBold', maxw=mm(74))
    # 姓名 + 职位 + 编号；BLANK = 通用证，姓名处留线，现场用白色油漆笔手写
    ny = mm(93) if title else mm(95)
    if name != 'BLANK':
        size = fit(name, 20, 'ExtraBold', mm(54))
        a.text(mm(8), ny, name, size, PAPER, 'ExtraBold', maxw=mm(54))
    else: a.line(mm(8), ny+mm(1), mm(58), ny+mm(1), SUB, .6)
    if title: a.text(mm(8), mm(99.5), title, 8, MUTED, 'Bold', maxw=mm(74))
    a.text(mm(82), ny, f'No. {serial:04d}', 7.5, MUTED, 'Bold', 'end')
    # 撕票线（印刷效果，不模切）
    a.line(mm(4), mm(103), mm(86), mm(103), LINE, .8, (mm(.4), mm(1.2)))
    zone_boxes(a, zone_states(role, zones), mm(107))
    return a


def back(role='STAFF', serial=1):
    spec = ROLES[role]; a = Art(W, H, SURFACE)
    # 顶部身份条：工牌翻面时也能一眼看出身份
    a.rect(0, 0, W, mm(30), spec['band'])
    if 'border' in spec:
        sw = spec['sw']; a.rect(sw/2, sw/2, W-sw, mm(30)-sw, None, stroke=spec['border'], sw=sw)
    a.text(mm(8), mm(21.5), spec['cn'], 16, spec['fg'], 'Heavy')
    a.text(mm(8), mm(27), role, 8, spec['fg'], 'ExtraBold')
    a.text(mm(8), mm(37.5), '通行区域', 9, PAPER, 'Bold'); a.text(mm(82), mm(37.5), 'ACCESS ZONES', 7, MUTED, 'Bold', 'end')
    # 歌单式区域表：每个区域一首「曲目」
    a.line(mm(8), mm(40), mm(82), mm(40), LINE, .6)
    for i, (cn, en) in enumerate(ZONES, 1):
        y = mm(40 + i*10)
        a.text(mm(8), y-mm(3), f'{i:02d}', 16, PAPER, 'ExtraBold')
        a.text(mm(22), y-mm(3.4), cn, 11, PAPER, 'Bold')
        a.text(mm(82), y-mm(3.4), en, 8, MUTED, 'Bold', 'end')
        a.line(mm(8), y, mm(82), y, LINE, .6)
    # 图例
    y = mm(85)
    a.rect(mm(8), y, mm(3.5), mm(3.5), PAPER, r=mm(.5)); a.text(mm(13), y+mm(2.9), '可进入', 7, MUTED)
    for xa, ya, xb, yb in [(0, 0, 3.5, 0), (3.5, 0, 3.5, 3.5), (3.5, 3.5, 0, 3.5), (0, 3.5, 0, 0)]:
        a.line(mm(32+xa), y+mm(ya), mm(32+xb), y+mm(yb), MUTED, .5, (mm(.6), mm(.4)))
    a.text(mm(37), y+mm(2.9), '按邀请', 7, MUTED)
    a.rect(mm(56), y, mm(3.5), mm(3.5), None, r=mm(.5), stroke=LINE, sw=.5); a.text(mm(61), y+mm(2.9), '不可进入', 7, MUTED)
    # 佩戴须知（中文在前，英文在后）
    a.text(mm(8), mm(96), '佩戴须知', 8, PAPER, 'Bold')
    rules = [('本证仅限本人使用，不可转借', 'Non-transferable.'),
             ('全程佩戴，保持可见', 'Wear it visibly at all times.'),
             ('遗失请立即告知现场负责人', 'Report a lost pass to the on-site lead.')]
    for i, (cn, en) in enumerate(rules):
        y = mm(102 + i*7.5)
        a.text(mm(8), y, cn, 7.5, PAPER, 'Regular', maxw=mm(74))
        a.text(mm(8), y+mm(3.2), en, 7, MUTED, 'Regular', maxw=mm(74))
    a.text(mm(8), mm(125), 'sinopop.us', 7, PAPER, 'Bold')
    a.text(mm(82), mm(125), f'No. {serial:04d}', 7, MUTED, 'Bold', 'end')
    return a


def pass_technical():
    a = Art(W, H, PAPER); a.rect(0, 0, W, H, None, r=mm(2.1), stroke=INK, sw=.5)
    a.rect(mm(38), mm(6), mm(14), mm(3), None, r=mm(1.5), stroke=INK, sw=.5)
    a.text(mm(9), mm(20), 'PVC 工牌 90 × 130 × 0.76 mm', 9, INK, 'Bold')
    for i, s in enumerate(['实线 = 外轮廓模切 + 挂孔（只此一张，不印在成品上）',
                           '圆角 R 2.1 mm · 挂孔 14 × 3 mm 长圆孔，居中，孔上沿距顶 6 mm',
                           '撕票线只是印刷效果，不打点线、不模切',
                           '右上圆圈 Ø 18 mm 为场次贴位，贴纸 Ø 16 mm',
                           '出血 3 mm；正反面同向（挂孔都在上）',
                           '姓名、编号为可变数据，按批量 PDF 逐张印']):
        a.text(mm(9), mm(30+i*8), s, 7, INK, 'Regular', maxw=mm(74))
    return a


def sticker(kind='odd', date='[MM.DD]'):
    bg, fg = STICKERS[kind]; a = Art(mm(16), mm(16), bg)
    a.circle(mm(8), mm(8), mm(6.9), None, stroke=fg, sw=.3)
    a.text(mm(8), mm(5.6), 'SHOW', 7, fg, 'Bold', 'middle')
    a.text(mm(8), mm(10.6), date, fit(date, 9, 'ExtraBold', mm(11.5), 7), fg, 'ExtraBold', 'middle')
    a.circle(mm(8), mm(13), mm(.45), fg)
    return a


def sticker_technical():
    a = Art(mm(16), mm(16), PAPER); a.circle(mm(8), mm(8), mm(8), None, stroke=INK, sw=.4)
    a.text(mm(8), mm(8.8), 'Ø 16', 7, INK, 'Bold', 'middle')
    return a


def lanyard_unit(kind):
    """一个循环单元：标志 · 英文身份 · 中文身份 · 刻度条。返回 (Art, 长度)。"""
    s = LANYARDS[kind]; logo_w = mm(17)
    x_en = logo_w + mm(5); en_w = width(s['en'], 15, 'ExtraBold')
    x_cn = x_en + en_w + mm(3.5); cn_w = width(s['cn'], 11, 'Bold')
    x_tick = x_cn + cn_w + mm(6); ticks = 9
    length = x_tick + ticks*mm(1.8) + mm(16)
    a = Art(length, mm(20), s['bg'])
    a.logo(0, mm(3.6), logo_w, s['logo'])
    a.text(x_en, mm(12.7), s['en'], 15, s['fg'], 'ExtraBold')
    a.text(x_cn, mm(12.4), s['cn'], 11, s['fg'], 'Bold')
    for i in range(ticks):
        h = mm(5) if i % 4 == 0 else mm(2.6)
        a.rect(x_tick + i*mm(1.8), mm(10)-h/2, mm(.6), h, s['fg'])
    return a, length


def lanyard(kind):
    """展开 900 × 20 mm。左右两半互为 180°，戴上后两侧都从工牌往脖子方向读。
    两端 15 mm 为夹片装配位，中间 50 mm 为颈后安全扣位，都不印字。"""
    s = LANYARDS[kind]; a = Art(mm(900), mm(20), s['bg'])
    unit, L = lanyard_unit(kind)
    lo, hi = mm(15+8), mm(450-25-8)
    n = int((hi-lo) // L); start = lo + ((hi-lo) - n*L)/2
    for i in range(n):
        a.place(unit, start + i*L, 0)
        a.place(unit, mm(900) - start - (i+1)*L, 0, rotation=180)
    return a


def lanyard_technical():
    a = Art(mm(900), mm(20), PAPER); a.rect(0, 0, a.w, a.h, None, stroke=INK, sw=.5)
    for x in (15, 885, 425, 475): a.line(mm(x), 0, mm(x), mm(20), INK, .5, (mm(1), mm(1)))
    a.text(mm(2), mm(12), '夹片', 7, INK, 'Bold')
    a.text(mm(887), mm(12), '夹片', 7, INK, 'Bold')
    a.text(mm(450), mm(12), '安全扣 50', 7, INK, 'Bold', 'middle')
    a.text(mm(30), mm(12), '展开 900 × 20 mm · 双面印 · 左半段正读，右半段旋转 180°（戴上后两侧都从工牌往上读）· 虚线外不印字', 8, INK, 'Regular')
    a.text(mm(490), mm(12), '两端 15 mm：哑黑金属夹片 + 龙虾扣 · 中间 50 mm：颈后安全扣（受力自动断开）', 8, INK, 'Regular')
    return a


def batch(csv_path, output):
    """CSV 列 name,role,zones，可选 no（编号，不填按行号）、title（职位，例「主理人 FOUNDER」）。
    name 写 BLANK 出通用证（姓名处留线手写）。输出一份多页 PDF：正、反、正、反……"""
    with open(csv_path, encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames or []
        if not {'name', 'role', 'zones'} <= set(cols) or not set(cols) <= {'no', 'name', 'title', 'role', 'zones'}:
            raise ValueError('CSV 列为 name,role,zones，可选 no,title')
        rows = list(reader)
    if not rows: raise ValueError('CSV 至少需要一条人员记录')
    arts, index, used = [], [], set()
    for i, row in enumerate(rows, 1):
        try:
            role = (row['role'] or '').strip().upper(); name = (row['name'] or '').strip()
            if role not in ROLES: raise ValueError('不支持的角色: '+role)
            if not name: raise ValueError('name 不能为空')
            if fit(name, 20, 'ExtraBold', mm(54)) <= 9 and width(name, 9, 'ExtraBold') > mm(54): raise ValueError('姓名过长')
            no = int(row.get('no') or i); title = (row.get('title') or '').strip()
            if no in used: raise ValueError(f'编号重复: {no}')
            used.add(no)
            arts += [front(role, name, row['zones'], no, title), back(role, no)]
            index.append(dict(no=f'{no:04d}', role=role, name=name, title=title, zones=zone_states(role, row['zones'])))
        except ValueError as exc:
            raise ValueError(f'CSV 第 {i+1} 行：{exc}') from exc
    output = Path(output); output.mkdir(parents=True, exist_ok=True)
    export_art(arts, output, 'passes-batch', 3, preview_long=1200)
    (output/'batch-index.json').write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8')


def main():
    OUT.mkdir(exist_ok=True)
    for role in ROLES:
        export_art([front(role), back(role)], OUT/'01-pass', 'pass-'+role.lower().replace(' ', '-'), 3)
    export_technical([pass_technical()], OUT/'01-pass', 'pass', 3)
    for kind in STICKERS: export_art([sticker(kind)], OUT/'02-show-sticker', 'sticker-'+kind, 1.5, preview_long=600)
    export_technical([sticker_technical()], OUT/'02-show-sticker', 'sticker', 1.5)
    for kind in LANYARDS:
        export_art([lanyard(kind), lanyard(kind)], OUT/'03-lanyard', 'lanyard-'+kind, 3, preview_long=5400)
    export_technical([lanyard_technical()], OUT/'03-lanyard', 'lanyard', 3)
    with (OUT/'people.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f); w.writerow(['name', 'role', 'zones'])
        for role, spec in ROLES.items(): w.writerow(['[姓名]', role, spec['zones']])
        w.writerow(['BLANK', 'STAFF', ''])
    batch(OUT/'people.csv', OUT/'04-batch-example')
    batch(OUT/'team-roster.csv', OUT/'06-team')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--batch', type=Path); p.add_argument('--output', type=Path)
    args = p.parse_args()
    if args.batch:
        if not args.output: p.error('--batch 需要 --output')
        batch(args.batch, args.output); print(args.output.resolve())
    else: main()
