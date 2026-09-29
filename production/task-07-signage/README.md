# 现场标识生产文件

每个物料的 `-rgb.pdf` 是 RGB 打样稿，`-print.pdf` 是 CMYK + SP-GREEN 专色印刷稿；同名 SVG 可编辑文字并嵌入字体子集，`-preview.png` 是 2400 px 长边预览。只有箭头使用亮绿，其他编号与环线为纸白或墨黑。深色大面板统一为层级面 #181A1F（墨黑提亮 3%）。英文使用灰色全大写。

| 文件前缀 | 成品尺寸 | 出血 | 工艺 |
|---|---:|---:|---|
| hang-restrooms / hang-bar-merch | 1200 × 300 mm | 5 mm | 技术 PDF 含外切与两枚直径 6 mm 吊孔；孔心距侧边 70 mm、距顶边 18 mm |
| entrance-ticket | 600 × 850 mm | 5 mm | 技术 PDF 含外切与两侧直径 30 mm 半圆缺口；印刷虚线是票根视觉语言 |
| wall-coat-check-a3 / wall-way-out-a3 | 297 × 420 mm | 3 mm | 直裁 |
| pillar-id-letter | 215.9 × 279.4 mm | 3 mm | 直裁 |
| house-rules | 600 × 900 mm | 5 mm | 直裁 |
| floor-photo-spot / floor-queue-start | 直径 600 mm | 5 mm | 技术 PDF 为圆形外切，方形 PDF 的 TrimBox 是外接框 |
| table-merch-a5 | 展开 148 × 515 mm；每面 148 × 210 mm | 5 mm | 双 A5 面板 210 + 210 mm，底座 80 mm，粘口 15 mm；首面在展开拼版中旋转 180°，两面顶部同在 y=210 mm 的屋脊折线；另两折线 y=420/500 mm |

`table-merch-a5-panel.svg` 是桌卡正面编辑副本；正式生产使用展开印刷 PDF。`sign-family-overview.svg/png` 为同物理比例的家族总览，只作审稿，不作为工厂尺寸依据。

`signage-height-qa.json` 记录每项功能词的实际汉字墨迹高度，依据 Noto Sans SC Heavy 字形边界计算。吊挂至少 100 mm、入口至少 150 mm、A3 墙贴至少 60 mm、Letter 立柱至少 30 mm、须知标题至少 40 mm/正文至少 15 mm、地贴至少 60 mm、桌卡至少 15 mm。辅助编号与英文不替代功能词。

须知五条规则、年龄限制、桌卡商品和价格全部是方括号占位；未填写任何活动日期或场地。切线、吊孔、折线只放在技术 PDF，印刷面没有工程线。亮绿建议用荧光专色 SP-GREEN，需实物打样比对；无任何供应商色号。墨黑或层级面材料上的纸白印刷要由印厂制作白墨版。方向牌仅用于运营导向，法定疏散标识沿用场馆已有设施。
