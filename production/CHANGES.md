# CHANGES — sinoPOP 局部修订

这是只包含修改项与新增专色文件的补丁包。目录与原交付对应，将本包内容合并到原交付根目录即可；不要删除未包含的旧文件。原交付目录和原 ZIP 在本次工作中没有被覆盖。任务三全部氛围图、生成底图、两份原始标志、原有字体与未涉及的工艺文件均未修改。

## 修订内容

1. **现场五图文字基线。** `task-02-onsite/compose-onsite.py` 改为按中英文连续字串分段，以 `anchor='ls'` 共用基线；不再逐字使用 `lt`。整段英文保留单词内部字距。五张 PNG 均从原 `_raw` 重合成，尺寸仍为 3072 × 2048。98 行文字经过 13 页 100% 原像素裁片逐行目视与独立复核，涵盖中点、句点、连字符、撇号、小写 i 及中英混排。底图没有重新生成。
2. **中文字重。** 从原 Noto Sans SC 可变字体新增 Regular 400、Medium 500、Bold 700 三个真实静态实例。六个名片方向和五张现场图按大小与同行英文字重重排：大号姓名/标题 Heavy；小号中文与 Archivo Regular 同行用 Regular，与 Archivo Bold 同行用 Bold。Medium 500 随包提供，不强行用于不需要的地方。相关 SVG 重新嵌入 WOFF2 字体子集，PDF 重新嵌入实际 TTF 子集；文字仍可编辑。受影响的名片内卡、J-card 展开稿、RGB 文件与产品效果图同步更新。
3. **04 后台证名片。** 正面绿色带改为“主办方 PROMOTER”；背面移除“后台通行证 / ALL ACCESS”，只留原白标、域名与结构孔位。避免名片和真实全区通行证混淆。任务二真实证件与手环的 ALL ACCESS 保留。
4. **01 票根正面。** 删除原标志右侧重复的 sinoPOP 文字，平面稿、PDF、效果图及总览同步更新。
5. **新增印刷分色版本。** 01 票根、02 歌单、06 材质各增加 `print-cmyk-spot.pdf`。现有 RGB 打样稿保留 RGB 模式并同步文字修订。新增文件的亮绿使用实际 `/Separation /SP-GREEN` 专色通道，以 `scn/SCN` 绘制；其余绘色均为 DeviceCMYK。未指定任何厂商色号。06 基于不含压凹灰字的 `ink-print.pdf`；姓名盲压凹继续使用未修改的独立 `deboss-mask.pdf`。

**亮绿建议用荧光专色，需实物打样比对。** SP-GREEN 的 CMYK 替代色仅用于屏幕预览；四色转换未套用特定印厂 ICC，非 PDF/X 认证。06 黑棉纸仍需印厂依据原白色对象另制不透明白墨版，并安排刷边、压凹工艺，本次 CMYK + SP-GREEN PDF 不定义白墨通道。

## 验证

- 已重新运行 `qa-summary.json`，全量检查 25 SVG、21 PDF 与原有 17 张最终 PNG。
- 独立校验确认色值、原始标志哈希、实际字体嵌入、最小 7 pt、TrimBox、9 pt 出血均通过。
- 3 份专色 PDF 的字体流、非颜色矢量操作与页面框保持；SP-GREEN 实际墨版非空，其余绘色无 RGB。
- 现场 98 行原像素基线检查通过；12 张名片平面、6 张产品效果、5 张现场全图完成目视复核。
- 原交付文件与受保护文件哈希未变化；本补丁每一项均为新增或与原版不同的文件，没有重复交回未修改的成品。
- `manifest.json` 为应用补丁后的整体交付清单；`patch-manifest.json` 只列本补丁文件及 SHA-256。内部 QA 裁片、缓存、原始生成图和工作副本未打包。

## 本次交回文件

- `README.md`
- `assets/fonts/NotoSansSC-Bold.ttf`
- `assets/fonts/NotoSansSC-Medium.ttf`
- `assets/fonts/NotoSansSC-Regular.ttf`
- `build_cards.py`
- `build_spot.py`
- `preview.png`
- `qa-cards.json`
- `qa-spot.json`
- `qa-summary.json`
- `qa/revision-validation.json`
- `qa/visual-review.json`
- `receipt-mockups.json`
- `task-01-cards/01-ticket/back-preview.png`
- `task-01-cards/01-ticket/back.svg`
- `task-01-cards/01-ticket/front-preview.png`
- `task-01-cards/01-ticket/front.svg`
- `task-01-cards/01-ticket/mockup.png`
- `task-01-cards/01-ticket/print-cmyk-spot.pdf`
- `task-01-cards/01-ticket/print.pdf`
- `task-01-cards/01-ticket/size-90x54-check.pdf`
- `task-01-cards/02-setlist/back.svg`
- `task-01-cards/02-setlist/front-preview.png`
- `task-01-cards/02-setlist/front.svg`
- `task-01-cards/02-setlist/mockup.png`
- `task-01-cards/02-setlist/print-cmyk-spot.pdf`
- `task-01-cards/02-setlist/print.pdf`
- `task-01-cards/02-setlist/size-90x54-check.pdf`
- `task-01-cards/03-vinyl/back-preview.png`
- `task-01-cards/03-vinyl/back.svg`
- `task-01-cards/03-vinyl/front.svg`
- `task-01-cards/03-vinyl/insert-back.svg`
- `task-01-cards/03-vinyl/insert-front.svg`
- `task-01-cards/03-vinyl/insert-print.pdf`
- `task-01-cards/03-vinyl/mockup.png`
- `task-01-cards/03-vinyl/print.pdf`
- `task-01-cards/03-vinyl/size-90x54-check.pdf`
- `task-01-cards/03-vinyl/sleeve-ink-print.pdf`
- `task-01-cards/04-backstage/back-preview.png`
- `task-01-cards/04-backstage/back.svg`
- `task-01-cards/04-backstage/front-preview.png`
- `task-01-cards/04-backstage/front.svg`
- `task-01-cards/04-backstage/mockup.png`
- `task-01-cards/04-backstage/print.pdf`
- `task-01-cards/04-backstage/size-90x54-check.pdf`
- `task-01-cards/05-jcard/back-preview.png`
- `task-01-cards/05-jcard/back.svg`
- `task-01-cards/05-jcard/construction.pdf`
- `task-01-cards/05-jcard/front.svg`
- `task-01-cards/05-jcard/mockup.png`
- `task-01-cards/05-jcard/print.pdf`
- `task-01-cards/05-jcard/size-90x54-check.pdf`
- `task-01-cards/05-jcard/spread-inside.svg`
- `task-01-cards/05-jcard/spread-outside.svg`
- `task-01-cards/06-material/back-preview.png`
- `task-01-cards/06-material/back.svg`
- `task-01-cards/06-material/front.svg`
- `task-01-cards/06-material/ink-print.pdf`
- `task-01-cards/06-material/print-cmyk-spot.pdf`
- `task-01-cards/06-material/print.pdf`
- `task-01-cards/06-material/size-90x54-check.pdf`
- `task-02-onsite/baseline-qa.json`
- `task-02-onsite/compose-onsite.py`
- `task-02-onsite/onsite-01-entrance.png`
- `task-02-onsite/onsite-02-lobby.png`
- `task-02-onsite/onsite-03-now-playing.png`
- `task-02-onsite/onsite-04-kit.png`
- `task-02-onsite/onsite-05-photo-spot.png`
- `task-02-onsite/receipt-onsite.json`
- `validate_revision.py`
- `CHANGES.md`
- `manifest.json`
- `patch-manifest.json`
