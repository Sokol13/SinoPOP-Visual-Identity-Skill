# 新现场套件俯拍效果图

工具：内置 ImageGen。空白底图后期用 `compose-credentials.py` 合成真实字体与原 SVG 标志。`onsite-04-kit.png` 为 3072 × 2048 PNG，仅为虚构 AI 场景示意。所有姓名、日期、场地、艺人、流程时间均保持占位；流水号为示例生产序号。

English prompt:

Photorealistic overhead flat-lay of a fictional concert operations kit on dark textured concrete, landscape 3:2. Camera perpendicular, printed faces flat for accurate typography compositing. All objects completely blank, no letters, numbers or logos. Left 68 percent: three narrow Tyvek wristbands aligned horizontally above the cards, top off-white, second vivid green #73F64B, third near-black #111318, adhesive ends on the right. Below, exactly six midnight navy #141926 portrait credential cards, proportion 90:130, small rounded corners and top horizontal lanyard holes, in a regular three-column, two-row grid. All faces unobstructed. Top row lanyards above cards are green, black, black; bottom row are off-white, gray, gray. Right 28 percent: large blank paper-white setlist sheet attached with torn green stage tape, one green tape roll and a black marker. Neutral studio side light, Tyvek and nylon texture, subtle shadows and film grain. No humans or typography. Four lanyard colors in total.

后期以共同基线合成所有连续字体字串。按 100% 原始像素逐行裁图检查；记录在 `_qa/credentials-text-baselines.json`。灰色挂绳实物折起，只露出循环字样的前段，完整循环见挂绳生产 SVG/PDF。尺寸与位置以正式印刷文件为准。
