# 品牌名改为 SinoPOP（2026-09-28）

只改品牌名写法：`sinoPOP` → `SinoPOP`。颜色、字体、字号、位置、版式、尺寸、出血、TrimBox/BleedBox、SP-GREEN 专色、刀模和工艺文件都没有改。文件名、文件夹名里的小写 `sinopop` 保持原样。

## 改了什么

| 范围 | 做法 |
|---|---|
| 生产脚本（`production.py`、`build_*.py`、`compose-*.py` 等 12 个） | 写死的品牌字符串和 PDF 元数据 `/Creator` 改为 SinoPOP |
| 名片内卡（task-04） | 重新生成 `insert-*`：封套圆标里的「SinoPOP」；`assembly-preview.png` 同步 |
| 挂绳（task-06） | 重新生成 4 款挂绳：「SinoPOP · STAFF / ARTIST / GUEST / PRESS / PRODUCTION」。循环间距不变，S 变宽后每组文字只宽约 0.6 mm，没有碰撞 |
| 主办方介绍（task-09） | 重新生成 A4 / Letter / 手机三套，页脚「SinoPOP · Promoter Profile」 |
| 现场效果图 `onsite-04-kit.png` | 用 `_raw/onsite-04-kit-blank.png` 重新合成，只替换 6 条挂绳上的文字区域，其余像素与上一版一致 |
| 工牌、手环、标识、易拉宝 | 画面上本来没有品牌字，重新导出后只有 PDF 元数据变化，逐页渲染与上一版完全相同 |
| 标志 SVG | 只改 `aria-label`，图形不变（与 skill 里的标志文件一致） |
| README / CHANGES / prompts / receipts / QA 说明 | 文字里的品牌名 |

## 没有改的

- `task-01-cards`：第一轮 6 个名片方向是存档，保持原样（包括 03-vinyl 样机上的旧写法）。
- `qa/` 里第一、二轮的 QA 记录只改了品牌名文字，数值没有重跑覆盖。

## 验证

- `qa/qa-brandname.json`：除 task-01 存档外，所有文本文件、SVG、PDF 文字和元数据里都没有 sinoPOP / Sinopop / SinoPop → PASS。
- 所有改动过的 PDF 和 PNG 都与上一版逐页渲染对比：差异只出现在品牌字位置；页面尺寸和页框不变。
- `qa_round2.py` 结果与改动前完全一样（task-02-onsite 的提示词文档里本来就有「不要写 ALL ACCESS」这类反例说明，改动前后都会被标记，不是这次引入的）。
