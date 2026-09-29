# 手环生产文件

成品 250 × 25 mm，Tyvek 一次性手环；右端 38 mm 为粘扣区。每个单条文件有 3 mm 出血和裁切线，PDF 的 TrimBox 为成品尺寸，BleedBox 为 256 × 31 mm。刀模及粘扣边界单独放在 `wristband-technical.pdf`。

- `wristband-ga-*`：纸白 GA，普通入场 · 早鸟同档。
- `wristband-vip-*`：亮绿 VIP，贵宾。
- `wristband-svip-*`：墨黑 SVIP，至尊 · 卡座。
- `*-rgb.pdf` 为屏幕/RGB 打样；`*-print.pdf` 为 CMYK + SP-GREEN 生产文件；同名 SVG 是嵌入实际字体子集及原 SVG 标志的可编辑版；`*-preview.png` 为无出血预览。
- `batch-example/` 是每档 2 条的脚本验收样张，A3 297 × 420 mm 拼版，每页至多 11 条。每条独立 3 mm 出血；条间留白 8–9 mm，外围可见裁切短线。全页另有 3 mm 出血和页面框。对应技术 PDF 给出每条裁边及粘扣边界。
- `wristbands-mockup.png` 是 AI 生成的虚构三腕效果图，后期合成真实标志与字体，不代表真实演出。

`[MM.DD]`、`[场地]` 是待填占位；6 位流水号是生产序列演示，不代表售票数量。默认编号段起点：GA 000001、VIP 100001、SVIP 200001。脚本拒绝编号重叠与超出六位范围。示例 `quantities.csv` 只用于测试，不是订单。

在交付根目录运行：

```powershell
python task-05-wristbands/batch-wristbands.py --csv task-05-wristbands/quantities.csv --output task-05-wristbands/generated
python task-05-wristbands/batch-wristbands.py --ga 100 --vip 30 --svip 10 --output task-05-wristbands/generated
```

依赖及字体放在交付根目录，脚本复用 `production.py` 与 `build_credentials.py`。需先在 `build_credentials.py` 的 `wristband` 中替换日期/场地占位，再运行批量；请勿在已生成 PDF 上覆盖序号。

字体为 Archivo Regular/Bold/ExtraBold 与 Noto Sans SC Regular/Bold/Heavy；中英混排共用基线。色值以交付根目录色表为准。亮绿建议用荧光专色，需实物打样比对；SP-GREEN 不指定厂家色号。深色 Tyvek 的白标和白字必须用白墨；荧光绿按承印材质确认遮盖力与白墨底。粘扣须为防转移结构，粘扣方向、拉断方式和号码可读性由加工厂实样核对。电子 PDF 的纸白色不构成白墨分版。
