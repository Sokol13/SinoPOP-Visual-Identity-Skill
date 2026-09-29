"""从已修订的 RGB 矢量母稿派生 CMYK + SP-GREEN 印刷文件。"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

import numpy as np
import pymupdf
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    ArrayObject, ContentStream, DictionaryObject, FloatObject, NameObject,
    NumberObject,
)

ROOT = Path(__file__).resolve().parent
GREEN = (0x73 / 255, 0xF6 / 255, 0x4B / 255)
JOBS = [('01-ticket', 'print.pdf'), ('02-setlist', 'print.pdf'),
        ('06-material', 'ink-print.pdf')]
COLOR_OPS = {b'rg', b'RG', b'g', b'G', b'k', b'K', b'cs', b'CS',
             b'sc', b'SC', b'scn', b'SCN'}
PAINT_OPS = {b'Tj', b'TJ', b"'", b'"'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def numeric(values):
    return [FloatObject(round(float(v), 8)) for v in values]


def rgb_to_cmyk(rgb):
    # 未采用印厂 ICC；使用透明、可复算的无配置文件换算，不能称为打样匹配。
    r, g, b = (min(1.0, max(0.0, float(v))) for v in rgb)
    k = 1.0 - max(r, g, b)
    if k >= 1.0 - 1e-9:
        return (0.0, 0.0, 0.0, 1.0)
    return ((1-r-k)/(1-k), (1-g-k)/(1-k), (1-b-k)/(1-k), k)


def separation(black_plate=False):
    # /SP-GREEN 是唯一专色名称；C1 只服务屏幕替代显示，不是供应商油墨色号。
    c1 = (0, 0, 0, 1) if black_plate else rgb_to_cmyk(GREEN)
    tint = DictionaryObject({
        NameObject('/FunctionType'): NumberObject(2),
        NameObject('/Domain'): ArrayObject(numeric([0, 1])),
        NameObject('/C0'): ArrayObject(numeric([0, 0, 0, 0])),
        NameObject('/C1'): ArrayObject(numeric(c1)),
        NameObject('/N'): NumberObject(1),
    })
    return ArrayObject([NameObject('/Separation'), NameObject('/SP-GREEN'),
                        NameObject('/DeviceCMYK'), tint])


def all_streams(reader):
    # 当前母稿全部是页面矢量，不包含外部图片、XObject 或着色器；异常时停下。
    for page in reader.pages:
        res = page['/Resources'].get_object()
        if res.get('/XObject') or res.get('/Shading') or res.get('/Pattern'):
            raise ValueError('Unexpected XObject / Shading / Pattern: explicit conversion required')
        yield page, ContentStream(page.get_contents(), reader)


def convert(src, dst):
    writer = PdfWriter(clone_from=src)
    count = Counter()
    for page, stream in all_streams(writer):
        new_ops = [([FloatObject(0), FloatObject(0), FloatObject(0), FloatObject(1)], b'k'),
                   ([FloatObject(0), FloatObject(0), FloatObject(0), FloatObject(1)], b'K')]
        for args, op in stream.operations:
            if op in (b'rg', b'RG'):
                stroke = op == b'RG'
                rgb = tuple(map(float, args))
                if all(abs(a-b) < 0.00001 for a, b in zip(rgb, GREEN)):
                    new_ops.append(([NameObject('/SPGreen')], b'CS' if stroke else b'cs'))
                    new_ops.append(([FloatObject(1)], b'SCN' if stroke else b'scn'))
                    count['spot_stroke' if stroke else 'spot_fill'] += 1
                else:
                    new_ops.append((numeric(rgb_to_cmyk(rgb)), b'K' if stroke else b'k'))
                    count['rgb_to_cmyk'] += 1
            elif op in (b'g', b'G'):
                new_ops.append((numeric([0, 0, 0, 1-float(args[0])]), b'K' if op == b'G' else b'k'))
                count['gray_to_cmyk'] += 1
            elif op in (b'cs', b'CS', b'sc', b'SC', b'scn', b'SCN'):
                raise ValueError(f'Unexpected source color operator {op!r}; review required')
            else:
                new_ops.append((args, op))
        stream.operations = new_ops
        page[NameObject('/Contents')] = writer._add_object(stream)
        page['/Resources'][NameObject('/ColorSpace')] = DictionaryObject({
            NameObject('/SPGreen'): separation(),
        })
    writer.add_metadata({
        '/Title': 'sinoPOP | CMYK + SP-GREEN print artwork',
        '/Subject': 'Process CMYK plus SP-GREEN separation; alternate preview only; printer selects ink; not PDF/X or ICC certified',
        '/Creator': 'sinoPOP visual production / build_spot.py',
    })
    writer.write(dst)
    return dict(count)


def stable_operations(reader):
    # 所有非颜色操作保持原样，因此文字、logo 贝塞尔路径、坐标、裁切线均不重绘。
    result = []
    for page, stream in all_streams(reader):
        result.append(repr([(args, op) for args, op in stream.operations if op not in COLOR_OPS]))
    return result


def fonts_in_use(reader):
    result = []
    for i, (page, stream) in enumerate(all_streams(reader)):
        font = None
        size = None
        used = set()
        for args, op in stream.operations:
            if op == b'Tf':
                font, size = str(args[0]), float(args[1])
            elif op in PAINT_OPS:
                used.add((font, size))
        for key, size in sorted(used):
            fd = page['/Resources']['/Font'][key].get_object()
            descendant = fd.get('/DescendantFonts')
            desc = (descendant[0].get_object() if descendant else fd).get('/FontDescriptor')
            desc = desc.get_object() if desc else {}
            data = next((desc[n].get_object().get_data() for n in ['/FontFile', '/FontFile2', '/FontFile3'] if n in desc), None)
            result.append({'page': i+1, 'key': key, 'name': str(fd['/BaseFont']),
                           'size_pt': size, 'embedded': data is not None,
                           'subset': '+' in str(fd['/BaseFont']),
                           'font_stream_sha256': sha(data) if data else None})
    return result


def plate_qa(path):
    writer = PdfWriter(clone_from=path)
    # 测试副本中把四色置为空白、专色置为黑；渲染实际内容并统计非空墨版面积。
    for page, stream in all_streams(writer):
        for args, op in stream.operations:
            if op in (b'k', b'K'):
                args[:] = numeric([0, 0, 0, 0])
        page[NameObject('/Contents')] = writer._add_object(stream)
        page['/Resources']['/ColorSpace'][NameObject('/SPGreen')] = separation(True)
    import io
    buf = io.BytesIO()
    writer.write(buf)
    doc = pymupdf.open(stream=buf.getvalue(), filetype='pdf')
    counts = []
    for page in doc:
        pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2), colorspace=pymupdf.csGRAY)
        counts.append(int((np.frombuffer(pix.samples, dtype=np.uint8) < 128).sum()))
    if not any(counts):
        raise ValueError(f'Empty SP-GREEN plate: {path}')
    return counts


def verify(src, dst, conversions):
    before = PdfReader(src)
    after = PdfReader(dst)
    assert stable_operations(before) == stable_operations(after), 'Non-color graphics operations changed'
    source_fonts = fonts_in_use(before)
    output_fonts = fonts_in_use(after)
    assert source_fonts == output_fonts, 'Text fonts / subsets changed in conversion'
    assert all(x['embedded'] and x['subset'] for x in output_fonts), 'Used font not embedded subset'
    assert min(x['size_pt'] for x in output_fonts) >= 7, 'Minimum 7 pt failed'
    assert [p.extract_text() for p in before.pages] == [p.extract_text() for p in after.pages]
    boxes = []
    spot_usage = []
    process_colors = set()
    for p0, (p1, stream) in zip(before.pages, all_streams(after)):
        box = {b: list(map(float, getattr(p1, b))) for b in ['mediabox', 'trimbox', 'bleedbox']}
        assert box == {b: list(map(float, getattr(p0, b))) for b in box}
        boxes.append(box)
        ops = Counter(op.decode('ascii') for _, op in stream.operations)
        assert not any(op in ops for op in ['rg', 'RG', 'g', 'G', 'sc', 'SC'])
        cs = p1['/Resources']['/ColorSpace']
        assert set(cs) == {'/SPGreen'}
        assert list(cs['/SPGreen'])[:3] == ['/Separation', '/SP-GREEN', '/DeviceCMYK']
        assert all(args == [1] for args, op in stream.operations if op in [b'scn', b'SCN'])
        assert all(args == ['/SPGreen'] for args, op in stream.operations if op in [b'cs', b'CS'])
        process_colors.update(tuple(map(float, args)) for args, op in stream.operations if op in [b'k', b'K'])
        spot_usage.append({'page': len(spot_usage)+1, 'fill_scn': ops.get('scn', 0), 'stroke_SCN': ops.get('SCN', 0)})
    # 整个交付文件不得残留 RGB/Gray 色彩空间绘制名称（字体二进制可能含无关文本，不扫字体）。
    for _, stream in all_streams(after):
        assert b'/DeviceRGB' not in stream.get_data()
    render_dir = ROOT/'_qa-spot'
    render_dir.mkdir(exist_ok=True)
    render_doc = pymupdf.open(dst)
    render_paths = []
    for i, page in enumerate(render_doc):
        p = render_dir/f'{dst.parent.name}-spot-page-{i+1}.png'
        page.get_pixmap(matrix=pymupdf.Matrix(4, 4), alpha=False).save(p)
        render_paths.append(str(p.relative_to(ROOT)))
    return {'file': str(dst.relative_to(ROOT)), 'source': str(src.relative_to(ROOT)),
            'sha256': sha(dst.read_bytes()), 'source_sha256': sha(src.read_bytes()),
            'pages': len(after.pages), 'conversions': conversions,
            'non_color_operators_unchanged': True, 'text_unchanged': True,
            'font_streams_unchanged': True, 'fonts_embedded_and_subset': True,
            'used_fonts': output_fonts,
            'minimum_font_pt': min(x['size_pt'] for x in output_fonts),
            'page_boxes_preserved': boxes, 'spot_name': 'SP-GREEN',
            'spot_colorspace': '/Separation /SP-GREEN /DeviceCMYK',
            'spot_usage': spot_usage, 'spot_plate_dark_pixels_144dpi': plate_qa(dst),
            'process_cmyk_colors': sorted(process_colors),
            'no_rgb_or_gray_paint_operators': True, 'raster_images': 0,
            'renders': render_paths, 'render_verified_programmatically': True}


def main():
    records = []
    for folder, filename in JOBS:
        src = ROOT/'task-01-cards'/folder/filename
        dst = src.with_name('print-cmyk-spot.pdf')
        conversions = convert(src, dst)
        records.append(verify(src, dst, conversions))
    report = {
        'status': 'PASS', 'strategy': 'Rewrite only RGB/Gray color operators into CMYK or full-tint SP-GREEN. Preserve all text, font streams, Bezier paths, page boxes and clipping operators.',
        'source_green_rgb': '#73F64B', 'spot_name': 'SP-GREEN',
        'ink_selection': 'Printer selects fluorescent spot ink after physical proof; no manufacturer ink number prescribed.',
        'limitations': [
            'CMYK conversion is mathematical and not characterized by a printer ICC profile; no colorimetric match claimed.',
            'SP-GREEN uses a DeviceCMYK alternate for screen preview only; this is not an ink formulation.',
            'Not a PDF/X-certified export.',
            '06-material is derived from ink-print.pdf and excludes blind-deboss names from the ink plate. The separate deboss-mask.pdf remains required.',
            '06-material still requires printer-specific opaque white ink, black cotton stock and edge-paint/deboss production setup; these CMYK+spot files do not define a white-ink separation.',
        ], 'files': records,
    }
    (ROOT/'qa-spot.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'status': report['status'], 'files': [r['file'] for r in records],
                      'spot_plate_pixels': [r['spot_plate_dark_pixels_144dpi'] for r in records]}, indent=2))


if __name__ == '__main__':
    main()
