"""可编辑的主办方介绍：A4、Letter 与手机竖版共用内容。"""
from pathlib import Path
import sys, json, base64, re, xml.etree.ElementTree as ET
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from production import Art, mm, width, export_art, INK, SURFACE, PAPER, GREEN, MUTED, SUB, LINE, PALE

OUT = Path(__file__).resolve().parent
KNOWN = '从华语青年音乐与文化出发，把现场带给海外的年轻观众。'
CHAPTERS = [('01', '我们是谁', 'WHO WE ARE', '03'),
            ('02', '我们做什么', 'WHAT WE DO', '04'),
            ('03', '做过的现场', 'PAST SHOWS', '05'),
            ('04', '合作方式与联系', 'HOW WE WORK · CONTACT', '06')]
SERVICES = [('活动主办与执行', 'EVENT PRODUCTION'),
            ('宣传推广', 'PROMOTION'), ('售票', 'TICKETING')]


def source_photo(name, fallback):
    # 优先使用已验收的原图；便携交付可从已内嵌图片的 SVG 还原输入。
    choices = [ROOT.parent/'sinopop-music-objects-20260927'/'task-03-profile'/name,
               ROOT/'task-03-profile'/name, OUT/'source-media'/name]
    for p in choices:
        if p.exists():
            return p
    svg = OUT/fallback
    if svg.exists():
        for element in ET.parse(svg).getroot().iter():
            href = element.get('{http://www.w3.org/1999/xlink}href', element.get('href', ''))
            if href.startswith('data:image/png;base64,'):
                target = ROOT/'_qa'/'profile-inputs'/name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(base64.b64decode(href.split(',', 1)[1]))
                return target
    raise FileNotFoundError(f'缺少已验收封面图：{name}')


def label(a, x, y, s, size=9, color=SUB, weight='Bold'):
    a.text(x, y, s, size, color, weight)


def footer(a, page, dark=False):
    m = 44
    color = MUTED if dark else SUB
    a.line(m, a.h-45, a.w-m, a.h-45, LINE if dark else PALE, .7)
    label(a, m, a.h-26, 'sinoPOP · 主办方介绍', 8, color, 'Regular')
    a.text(a.w-m, a.h-26, f'{page:02} / 06', 8, color, 'Bold', 'end')


def page_header(a, number, title, english, dark=False):
    color = PAPER if dark else INK
    label(a, 44, 54, f'曲目 {number} · TRACK {number}', 9, MUTED if dark else SUB)
    a.logo(a.w-93, 29, 49, 'white' if dark else 'black')
    a.text(44, 115, title, 36, color, 'ExtraBold')
    label(a, 45, 139, english, 10, MUTED if dark else SUB)
    a.line(44, 158, a.w-44, 158, GREEN if dark else INK, 2)


def paper_pages(w, h, square):
    m, span = 44, w-88
    pages = []
    a = Art(w, h, SURFACE)
    label(a, m, 42, 'sinoPOP · PROMOTER PROFILE', 8, MUTED)
    a.text(w-m, 42, 'SIDE A · [年份]', 8, MUTED, 'Bold', 'end')
    top = 64
    a.image(m, top, span, span, square)
    a.logo(m+18, top+span-86, 86, 'white')
    a.text(m, top+span+57, '主办方介绍', 43, PAPER, 'ExtraBold')
    label(a, m+1, top+span+81, 'Promoter Profile', 14, MUTED)
    # Letter 较矮，因此正文按固定底边基线排版。
    label(a, m, h-81, '从华语青年音乐与文化出发，', 10.5, MUTED, 'Regular')
    label(a, m, h-65, '把现场带给海外的年轻观众。', 10.5, MUTED, 'Regular')
    label(a, m, h-30, '封面为 AI 氛围图 · 非真实活动记录', 7.5, MUTED, 'Regular')
    a.text(w-m, h-30, '[版本] · [YYYY.MM]', 8, MUTED, 'Regular', 'end')
    pages.append(a)

    a = Art(w, h, PAPER)
    a.text(m, 81, '曲目', 43, INK, 'ExtraBold')
    label(a, m+1, 102, 'TRACKLIST', 10)
    a.logo(w-110, 38, 66, 'black')
    a.line(m, 127, w-m, 127, INK, 2.5)
    for i, (n, cn, en, p) in enumerate(CHAPTERS):
        y = 180+i*87
        a.text(m, y, n, 26, INK, 'ExtraBold')
        a.text(m+65, y-2, cn, 22, INK, 'ExtraBold')
        label(a, m+66, y+19, en, 8.5)
        a.text(w-m, y+1, f'p.{p}', 9, SUB, 'Bold', 'end')
        a.line(m, y+37, w-m, y+37, PALE, .8)
    label(a, m, h-230, '说明 · LINER NOTES', 9)
    label(a, m, h-204, '从华语青年音乐与文化出发，', 12, INK, 'Regular')
    label(a, m, h-184, '把现场带给海外的年轻观众。', 12, INK, 'Regular')
    chips = [('活动主办与执行', 146), ('宣传推广', 109), ('售票', 77)]
    x = m
    for text, ww in chips:
        a.rect(x, h-139, ww, 31, GREEN if text=='售票' else PAPER, r=6, stroke=None if text=='售票' else INK, sw=1)
        a.text(x+ww/2, h-118, text, 10, INK, 'Bold', 'middle')
        x += ww+12
    footer(a, 2)
    pages.append(a)

    a = Art(w, h, SURFACE)
    page_header(a, '01', '我们是谁', 'WHO WE ARE', True)
    a.text(m, 281, '从华语青年音乐与文化出发，', 24, PAPER, 'ExtraBold')
    a.text(m, 324, '把现场带给海外的年轻观众。', 24, PAPER, 'ExtraBold')
    label(a, m, 390, '说明 · LINER NOTES', 9, MUTED)
    a.line(m, 410, w-m, 410, LINE, .8)
    fields = [('[团队介绍]', '[团队介绍正文]'), ('[文化与受众]', '[文化与受众说明]'), ('[工作方式]', '[工作方式说明]')]
    for i, (title, content) in enumerate(fields):
        y = 461+i*82
        a.text(m, y, title, 16, PAPER, 'Bold')
        label(a, m, y+26, content, 11, MUTED, 'Regular')
    footer(a, 3, True)
    pages.append(a)

    a = Art(w, h, PAPER)
    page_header(a, '02', '我们做什么', 'WHAT WE DO')
    for i, (cn, en) in enumerate(SERVICES):
        y = 196+i*163
        a.rect(m, y, span, 137, SURFACE, r=6)
        a.text(m+18, y+45, f'{i+1:02}', 26, GREEN, 'ExtraBold')
        a.text(m+82, y+43, cn, 22, PAPER, 'ExtraBold')
        label(a, m+83, y+64, en, 9, MUTED)
        a.line(m+82, y+82, w-m-20, y+82, LINE, .7)
        label(a, m+82, y+109, '[服务说明与合作范围]', 11, PAPER, 'Regular')
    footer(a, 4)
    pages.append(a)

    a = Art(w, h, SURFACE)
    page_header(a, '03', '做过的现场', 'PAST SHOWS', True)
    label(a, m, 184, '必须用真实活动照片并注明摄影；不得以 AI 氛围图代替。', 9, MUTED, 'Regular')
    for i in range(2):
        y = 211+i*260
        a.rect(m, y, span, 171, None, r=6, stroke=SUB, sw=1)
        a.text(w/2, y+88, '[真实活动照片]', 20, PAPER, 'Bold', 'middle')
        a.text(w/2, y+111, '[摄影：姓名]', 10, MUTED, 'Regular', 'middle')
        label(a, m, y+198, '[艺人名] · [日期] · [场地]', 12, PAPER, 'Bold')
        label(a, m, y+221, '[活动说明] · 摄影：[姓名]', 9, MUTED, 'Regular')
    footer(a, 5, True)
    pages.append(a)

    a = Art(w, h, PAPER)
    page_header(a, '04', '合作方式与联系', 'HOW WE WORK · CONTACT')
    label(a, m, 202, '合作方式 · HOW WE WORK', 10, SUB)
    for i, txt in enumerate(['[合作方向]', '[合作范围与流程]', '[项目需求与下一步]']):
        y = 247+i*53
        a.text(m, y, txt, 18, INK, 'Bold')
        a.line(m, y+17, w-m, y+17, PALE, .8)
    a.rect(m, 414, span, 244, SURFACE, r=6)
    label(a, m+20, 449, '联系我们 · CONTACT', 10, MUTED)
    a.text(m+20, 489, '[联系人姓名]', 23, PAPER, 'ExtraBold')
    label(a, m+20, 512, '[职务] · [团队]', 10, MUTED, 'Regular')
    for i, txt in enumerate(['电话 PHONE · [电话号码]', '微信 WECHAT · [微信号]', '邮箱 EMAIL · [邮箱地址]']):
        label(a, m+20, 553+i*28, txt, 11, PAPER, 'Regular')
    label(a, m, h-101, '[合作邀请或补充说明]', 11, SUB, 'Regular')
    footer(a, 6)
    pages.append(a)
    return pages


def mobile_footer(a, page, dark=False):
    c = MUTED if dark else SUB
    a.line(80, 1813, 1000, 1813, LINE if dark else PALE, 2)
    a.text(80, 1864, 'sinoPOP · 主办方介绍', 27, c, 'Regular')
    a.text(1000, 1864, f'{page:02} / 06', 27, c, 'Bold', 'end')


def mobile_header(a, number, cn, en, dark=False):
    a.text(80, 110, f'曲目 {number} · TRACK {number}', 30, MUTED if dark else SUB, 'Bold')
    a.logo(850, 60, 150, 'white' if dark else 'black')
    # 合作页较长的标题分两行，避免压缩字体。
    if cn=='合作方式与联系':
        a.text(80, 267, '合作方式', 91, PAPER if dark else INK, 'ExtraBold')
        a.text(80, 380, '与联系', 91, PAPER if dark else INK, 'ExtraBold')
        a.text(80, 439, en, 30, MUTED if dark else SUB, 'Bold')
        a.line(80, 485, 1000, 485, GREEN if dark else INK, 5)
    else:
        a.text(80, 302, cn, 91, PAPER if dark else INK, 'ExtraBold')
        a.text(80, 366, en, 30, MUTED if dark else SUB, 'Bold')
        a.line(80, 425, 1000, 425, GREEN if dark else INK, 5)


def mobile_pages(phone):
    pages = []
    a = Art(1080, 1920, SURFACE)
    a.image(0, 0, 1080, 1920, phone)
    a.poly([(80, 91), (80, 125), (109, 108)], GREEN)
    a.text(132, 122, 'NOW PLAYING', 33, GREEN, 'Bold')
    a.logo(826, 68, 175, 'white')
    # 以平面层级面信息区保证阅读，同时保留原照片完整比例。
    a.rect(0, 1440, 1080, 480, SURFACE)
    a.text(80, 1576, '主办方介绍', 94, PAPER, 'ExtraBold')
    a.text(84, 1636, 'sinoPOP · Promoter Profile', 33, MUTED, 'Bold')
    a.line(80, 1700, 1000, 1700, LINE, 9)
    a.line(80, 1700, 240, 1700, GREEN, 9)
    a.circle(240, 1700, 10, GREEN)
    a.text(80, 1762, '01 / 06', 29, MUTED, 'Bold')
    a.text(1000, 1762, '往下看', 29, MUTED, 'Bold', 'end')
    a.text(80, 1864, 'AI 氛围图 · 非真实活动记录', 24, MUTED, 'Regular')
    pages.append(a)

    a = Art(1080, 1920, PAPER)
    a.text(80, 234, '曲目', 105, INK, 'ExtraBold')
    a.text(85, 299, 'TRACKLIST', 33, SUB, 'Bold')
    a.logo(840, 100, 160, 'black')
    a.line(80, 350, 1000, 350, INK, 6)
    for i, (n, cn, en, p) in enumerate(CHAPTERS):
        y = 516+i*234
        a.text(80, y, n, 67, INK, 'ExtraBold')
        a.text(222, y-7, cn, 52, INK, 'ExtraBold')
        a.text(226, y+48, en, 27, SUB, 'Bold')
        a.text(1000, y+93, f'p.{p}', 26, SUB, 'Bold', 'end')
        a.line(80, y+127, 1000, y+127, PALE, 2)
    a.text(80, 1550, '从华语青年音乐与文化出发，', 40, INK, 'Regular')
    a.text(80, 1613, '把现场带给海外的年轻观众。', 40, INK, 'Regular')
    mobile_footer(a, 2)
    pages.append(a)

    a = Art(1080, 1920, SURFACE)
    mobile_header(a, '01', '我们是谁', 'WHO WE ARE', True)
    for i, s in enumerate(['从华语青年音乐', '与文化出发，', '把现场带给海外的', '年轻观众。']):
        a.text(80, 600+i*111, s, 66, PAPER, 'ExtraBold')
    a.text(80, 1140, '说明 · LINER NOTES', 29, MUTED, 'Bold')
    for i, s in enumerate(['[团队介绍]', '[文化与受众说明]', '[工作方式说明]']):
        a.text(80, 1270+i*145, s, 46, PAPER, 'Regular')
        a.line(80, 1320+i*145, 1000, 1320+i*145, LINE, 2)
    mobile_footer(a, 3, True)
    pages.append(a)

    a = Art(1080, 1920, PAPER)
    mobile_header(a, '02', '我们做什么', 'WHAT WE DO')
    for i, (cn, en) in enumerate(SERVICES):
        y = 497+i*389
        a.rect(80, y, 920, 330, SURFACE, r=16)
        a.text(116, y+83, f'{i+1:02}', 61, GREEN, 'ExtraBold')
        a.text(267, y+83, cn, 59, PAPER, 'ExtraBold')
        a.text(271, y+144, en, 28, MUTED, 'Bold')
        a.line(269, y+180, 963, y+180, LINE, 2)
        a.text(269, y+246, '[服务说明与合作范围]', 36, PAPER, 'Regular')
    mobile_footer(a, 4)
    pages.append(a)

    a = Art(1080, 1920, SURFACE)
    mobile_header(a, '03', '做过的现场', 'PAST SHOWS', True)
    a.text(80, 490, '必须用真实活动照片并注明摄影。', 32, MUTED, 'Regular')
    a.text(80, 540, '不得以 AI 氛围图代替。', 32, MUTED, 'Regular')
    for i in range(2):
        y = 606+i*563
        a.rect(80, y, 920, 333, None, r=12, stroke=SUB, sw=2)
        a.text(540, y+167, '[真实活动照片]', 49, PAPER, 'Bold', 'middle')
        a.text(540, y+224, '[摄影：姓名]', 29, MUTED, 'Regular', 'middle')
        a.text(80, y+399, '[艺人名] · [日期] · [场地]', 38, PAPER, 'Bold')
        a.text(80, y+451, '[活动说明] · 摄影：[姓名]', 28, MUTED, 'Regular')
    mobile_footer(a, 5, True)
    pages.append(a)

    a = Art(1080, 1920, PAPER)
    mobile_header(a, '04', '合作方式与联系', 'HOW WE WORK · CONTACT')
    a.text(80, 567, '合作方式 · HOW WE WORK', 30, SUB, 'Bold')
    for i, txt in enumerate(['[合作方向]', '[合作范围与流程]', '[项目需求与下一步]']):
        a.text(80, 670+i*126, txt, 45, INK, 'Bold')
        a.line(80, 715+i*126, 1000, 715+i*126, PALE, 2)
    a.rect(80, 1070, 920, 620, SURFACE, r=16)
    a.text(125, 1150, '联系我们 · CONTACT', 30, MUTED, 'Bold')
    a.text(125, 1252, '[联系人姓名]', 61, PAPER, 'ExtraBold')
    a.text(125, 1314, '[职务] · [团队]', 30, MUTED, 'Regular')
    for i, txt in enumerate(['电话 PHONE · [电话号码]', '微信 WECHAT · [微信号]', '邮箱 EMAIL · [邮箱地址]']):
        a.text(125, 1430+i*85, txt, 34, PAPER, 'Regular')
    mobile_footer(a, 6)
    pages.append(a)
    return pages


def build():
    OUT.mkdir(exist_ok=True)
    square = source_photo('profile-cover-square.png', 'a4/profile-a4-p01.svg')
    phone = source_photo('profile-cover-phone.png', 'mobile/profile-mobile-p01.svg')
    data = {}
    for size, w, h in [('a4', mm(210), mm(297)), ('letter', 612, 792)]:
        arts = paper_pages(w, h, square)
        export_art(arts, OUT/size, f'profile-{size}', bleed_mm=3, preview_long=2400)
        data[size] = {'size_pt': [w, h], 'pages': 6, 'bleed_mm': 3,
                      'minimum_font_pt': min(op[4] for a in arts for op in a.ops if op[0]=='text')}
    arts = mobile_pages(phone)
    export_art(arts, OUT/'mobile', 'profile-mobile', bleed_mm=3, preview_long=1920)
    # 手机导出严格为指定像素，避免 PDF 渲染矩阵取整多出一个像素。
    for p in (OUT/'mobile').glob('*-preview.png'):
        with Image.open(p) as im:
            im.resize((1080, 1920), Image.Resampling.LANCZOS).save(p)
    for p in (OUT/'mobile').glob('*.svg'):
        s = p.read_text(encoding='utf-8')
        s = re.sub(r'width="[^"]+" height="[^"]+"', 'width="1080px" height="1920px"', s, count=1)
        p.write_text(s, encoding='utf-8')
    data['mobile'] = {'pixels': [1080, 1920], 'pages': 6, 'purpose': 'digital'}
    (OUT/'profile-metadata.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    return data


if __name__=='__main__':
    print(json.dumps(build(), ensure_ascii=False, indent=2))
