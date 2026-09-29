# 交接文件 · Google Docs / Sheets 样式指南

适用：需要和合作方一起在线编辑的事实卡、艺人交接单、报价单。对外定稿请用 Figma 模板导出 PDF 或长图。

## 一次性设置（Docs）
1. 字体：菜单「字体 → 更多字体」，添加 **Noto Sans SC**（即思源黑体 Source Han Sans SC；Google 字体菜单里叫 Noto Sans SC）和 **Archivo**。
2. 格式 → 段落样式，把下面几种样式设好，再用「更新 ‘…’ 以匹配」保存：

| 样式 | 字体 | 字号 | 颜色 |
|---|---|---|---|
| 标题 Title | Noto Sans SC Bold | 20 pt | #111318 |
| 标题 1 Heading 1 | Noto Sans SC Bold | 13 pt | #111318，前面手动加编号 01 / 02（颜色 #286C2A） |
| 正文 Normal text | Noto Sans SC Regular | 10.5 pt，行距 1.5 | #111318 |
| 说明 | Noto Sans SC Regular | 9 pt | #5A616C |

3. 英文和数字（日期、时间、价格）选中后改成 Archivo。
4. 页眉：左边放黑色标志（assets/sinopop-logo-black.svg 导出的 PNG），右边写「文件类型 · 版本 v01 · 更新 YYYY.MM.DD」。

## 表格（事实行、当日流程）
- 两列：左「标签 Label」（9 pt，#5A616C），右「内容」（10.5 pt，Medium）。
- 只留横线，线色 #D8DBD3，宽 1 pt；不要竖线、不要底色。
- 没核实的内容写「待确认 To be confirmed」，文字颜色 #5A616C（灰）。
- 当日流程四列：时间（HH:MM，Archivo Bold）｜事项｜负责人｜备注。

## Sheets
- 表头：Noto Sans SC Bold 10，底色 #F7F8F4，下边框 #D8DBD3。
- 日期列格式 `MM.DD ddd`，时间 `HH:mm`，金额 `"USD "#,##0`。
- 状态列只用这五个词：即将开售 / 售票中 / 时间调整 / 已售罄 / 已取消。

## 命名与版本
`SinoPOP_{类型}_{艺人}_{城市}_v01_YYYYMMDD` — 每次改动升一个版本号，并同步页眉日期。
