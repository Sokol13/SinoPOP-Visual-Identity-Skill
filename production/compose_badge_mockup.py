"""工牌 + 挂绳装配示意图（平面示意，不是照片）。读取 task-10-badge-kit 的预览图，输出 05-mockup/*.png。"""
from pathlib import Path
from PIL import Image, ImageDraw
from production import ROOT, INK, SURFACE, PAPER, SUB, LINE, PALE

KIT = ROOT/'task-10-badge-kit'; OUT = KIT/'05-mockup'
PX = 6.667                      # px / mm
PAIRS = [('staff', 'staff'), ('artist', 'artist'), ('artist-team', 'artist'), ('guest', 'guest'), ('press', 'press-production'), ('production', 'press-production')]


def strap(kind, left, length_mm):
    src = Image.open(KIT/f'03-lanyard/lanyard-{kind}-p01-preview.png').convert('RGB')
    s = src.width/900
    box = (int(15*s), 0, int((15+length_mm)*s), src.height) if left else (int((885-length_mm)*s), 0, int(885*s), src.height)
    seg = src.crop(box).resize((int(length_mm*PX), int(20*PX)), Image.LANCZOS)
    return seg.rotate(90 if left else -90, expand=True)   # 工牌端朝下，两侧都从下往上读


def mockup(role, kind):
    import math
    W, H = 1400, 2300; img = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(img)
    cx = W//2; knot_y = 1130
    for left in (True, False):
        s = strap(kind, left, 180).convert('RGBA'); h = s.height
        th = 8 if left else -8; r = s.rotate(th, expand=True, resample=Image.BICUBIC)
        bx = r.width/2 + h/2*math.sin(math.radians(th)); by = r.height/2 + h/2*math.cos(math.radians(th))
        tx, ty = cx + (-28 if left else 28), knot_y + 20
        img.paste(r, (int(tx-bx), int(ty-by)), r)
    # 哑黑夹片 + 圆环 + 龙虾扣（示意）
    d.rounded_rectangle((cx-92, knot_y-20, cx+92, knot_y+60), 10, fill=INK, outline=LINE, width=3)
    d.line((cx-72, knot_y+20, cx+72, knot_y+20), fill=LINE, width=3)
    d.ellipse((cx-20, knot_y+56, cx+20, knot_y+96), outline=INK, width=9)
    d.rounded_rectangle((cx-30, knot_y+92, cx+30, knot_y+230), 30, outline=INK, width=14)
    d.rectangle((cx+16, knot_y+130, cx+31, knot_y+190), fill=PAPER)
    d.line((cx+23, knot_y+122, cx+23, knot_y+198), fill=SUB, width=6)
    # 工牌（挂孔镂空）
    card = Image.open(KIT/f'01-pass/pass-{role}-p01-preview.png').convert('RGB').resize((int(90*PX), int(130*PX)), Image.LANCZOS)
    mask = Image.new('L', card.size, 0); md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, card.width-1, card.height-1), int(2.1*PX), fill=255)
    md.rounded_rectangle((int(38*PX), int(6*PX), int(52*PX), int(9*PX)), int(1.5*PX), fill=0)
    top = knot_y + 222 - int(6*PX)
    img.paste(card, (cx-card.width//2, top), mask)
    # 扣钩从挂孔穿过：只露出孔内一段
    sy = top + int(6*PX)
    d.line((cx-26, sy+int(1.5*PX), cx+26, sy+int(1.5*PX)), fill=INK, width=12)
    OUT.mkdir(parents=True, exist_ok=True); img.save(OUT/f'mockup-{role}.png')


def team_sheet(folder='06-team'):
    """每人一组：正面 + 反面。"""
    pages = sorted((KIT/folder).glob('passes-batch-p*-preview.png'))
    cards = [Image.open(p).convert('RGB') for p in pages]
    w, h = cards[0].size; g = 40; cols = 6; rows = (len(cards)+cols-1)//cols
    sheet = Image.new('RGB', (cols*w+(cols+1)*g, rows*h+(rows+1)*g), PAPER)
    for i, c in enumerate(cards):
        sheet.paste(c, (g+(i % cols)*(w+g), g+(i//cols)*(h+g)))
    OUT.mkdir(parents=True, exist_ok=True); sheet.save(OUT/f'sheet-{folder}.png')


def pair(front, back, out):
    f = Image.open(KIT/front).convert('RGB'); b = Image.open(KIT/back).convert('RGB'); g = 60
    s = Image.new('RGB', (f.width*2+g*3, f.height+g*2), PAPER); s.paste(f, (g, g)); s.paste(b, (f.width+2*g, g)); s.save(OUT/out)


if __name__ == '__main__':
    for role, kind in PAIRS: mockup(role, kind)
    team_sheet()
    pair('06-team/passes-batch-p03-preview.png', '06-team/passes-batch-p04-preview.png', 'staff-front-back.png')
    pair('06-team/passes-batch-p09-preview.png', '06-team/passes-batch-p10-preview.png', 'door-front-back.png')
    pair('06-team/passes-batch-p17-preview.png', '06-team/passes-batch-p18-preview.png', 'tourcrew-front-back.png')
