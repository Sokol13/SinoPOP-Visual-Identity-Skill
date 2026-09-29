# 工牌与挂绳生产文件

工牌成品 90 × 130 mm，3 mm 出血，正面为第 1 页、背面区域图例为第 2 页。圆角 R 2.1 mm；顶端挂孔 14 × 3 mm、距顶 6 mm；具体刀具、孔位及扣件适配请先实样。孔与外轮廓只在 `pass-technical.pdf`，不印入正反面。

六款 `pass-*` 分别为 STAFF 主办团队、ARTIST 艺人、ARTIST TEAM 艺人团队、GUEST 嘉宾、PRESS 媒体、PRODUCTION 制作。大面积面板为层级面 #181A1F。身份条按角色采用亮绿、墨黑、纸白或辅助灰，艺人绿色内框为 3 pt，艺人团队绿色内框和制作灰内框均为 1 pt。

白格 = 可进入；空格 = 不可进入；虚线格 = 按邀请开放。默认权限：STAFF、ARTIST、ARTIST TEAM 为 1–4；GUEST 为 1、2 按邀请；PRESS 为 1；PRODUCTION 为 1–3。编号含义：1 场内 FLOOR、2 后台 BACKSTAGE、3 舞台 STAGE、4 艺人休息室 GREEN ROOM。

挂绳展开 900 × 20 mm，3 mm 出血，双面各一页；四款 `lanyard-*` 为绿色 STAFF、黑色 ARTIST（艺人与艺人团队共用）、纸白 GUEST、灰色 PRESS / PRODUCTION。`lanyard-technical.pdf` 标出外轮廓与两端 15 mm 装配预留，实际折返及扣件由加工厂确认。印刷文字在装配预留区之外，循环间距保持不变；禁止非等比缩放。

`*-rgb.pdf` 用于 RGB 打样，`*-print.pdf` 为 CMYK + SP-GREEN。SVG 含可编辑文字和真实嵌入字体子集；PNG 为无出血预览。`passes.csv` 只有 `[姓名]` 占位与默认身份/区域，没有真实人员信息。`batch-example` 包含这 6 条占位数据的实际执行输出。

批量命令（在交付根目录运行）：

```powershell
python task-06-passes-lanyards/batch-passes.py task-06-passes-lanyards/passes.csv --output task-06-passes-lanyards/generated
```

CSV 列固定为 `name,role,zones`。角色用以上 6 个英文名称。zones 用逗号分隔，在 CSV 中整体加双引号；`1,2?` 表示 1 可进、2 按邀请开放，省略的区域不可进；留空时采用角色默认区域。填写真实姓名与当场已确认权限后重新运行。文件名用递增编号避免暴露姓名。脚本校验未知角色、重复区域及越界数字。

CSV 必须至少包含一条人员记录。脚本先读取整份 CSV，检查每行列数、姓名、角色、区域及姓名在版面中的宽度，并成功构造全部正反面后才创建输出目录；任意一行无效都会报出行号并停止，不产生半套文件。已有输出目录中的历史文件不会因输入校验失败而改动。

亮绿建议用荧光专色，需实物打样比对；SP-GREEN 不指定具体色号。深色卡上的白字与白标需要白墨版，使用深色底材时由印厂另行建立白墨版并确认遮盖/套印；纸白底白卡上的深色满版则可由印厂选择常规 CMYK 工艺。电子 PDF 的纸白不等于白墨通道。挂绳请按织物印刷/热转印色样确认绿色和细字边缘。

`../task-02-onsite/onsite-04-kit.png` 是重做的虚构 AI 俯拍效果图，展示新三档手环、六种工牌、四色挂绳，标志与文字后期准确合成；不能作为真实活动记录。
