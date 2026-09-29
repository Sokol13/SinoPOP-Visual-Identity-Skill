# SinoPOP Visual Identity Skill · 视觉识别与设计规范 2.1

SinoPOP 的完整品牌规范，做成了 AI 能直接用的技能。装好以后，Claude、Codex、ChatGPT 做 sinoPOP 的任何东西——网页小组件、公众号文章、交接文件、名片、手环、工牌挂绳、现场标识、易拉宝、主办方介绍——都会按同一套 VI 和设计规范来。

**安装：看 [INSTALL.md](INSTALL.md)，按你用的工具复制一段提示词就行。**

## 里面有什么

```
AGENTS.md                         给 Codex / Cursor 等编程 AI 的入口
CLAUDE.md                         给 Claude Code 的入口（指向 AGENTS.md）
INSTALL.md                        各工具的一次性安装提示词
.claude-plugin/marketplace.json   Claude Code 插件市场清单（sinopop-design@sinopop）

skills/sinopop-design/            技能本体（Claude / Codex 通用）
  SKILL.md                        完整规则：硬规则、字级、状态、证件、印刷生产、tokens、组件 CSS、公众号模块
  scripts/check_brand.py          交付前自检：颜色是否都在规范里、停用色、禁用文案
  design-system/                  设计系统代码包
    tokens/                       颜色、字号、间距、圆角（tokens.json 为源，build.py 生成 tokens.css）
    web/                          网页小组件 CSS、示例页、可直接贴进 Wix 的嵌入代码
    wechat/                       公众号框架 A（自办）/ B（艺人）模板和头尾图
    handoff/                      交接文件在 Google Docs 里的样式
    assets/                       白 / 黑两版矢量标志、示例图

docs/
  sinoPOP-VI-2.1.pdf              VI 规范 30 页（给人看）
  sinoPOP-Design-Standards-2.1.pdf 设计规范 10 页
  CHANGELOG.md                    所有决定和改动记录
  surface-tint-X4.png             层级面底色选择对比

production/                       印刷与现场生产文件（先读 START-HERE.md）
  task-04 … task-09               定稿：名片封套、手环、工牌挂绳、标识、易拉宝、主办方介绍
  task-01 … task-03               第一轮探索与 AI 效果图（存档）
  build_*.py、requirements.txt    重新生成和批量输出的脚本

chatgpt/PROJECT-INSTRUCTIONS.md   ChatGPT 项目指令
dist/                             生成的安装包：Claude App 用的 zip、ChatGPT 项目文件
tools/build-dist.sh               改了技能以后重新生成 dist/
```

## 核心规则一览

- **颜色**：墨黑 `#111318` · 层级面 `#181A1F` · 纸白 `#F7F8F4` · 亮绿 `#73F64B` · 灰 `#B7BDC5` `#5A616C` `#3A3F48` `#D8DBD3`。状态只用单色 + 绿；粉色只做活动视觉点缀。
- **字体**：英文和数字 Archivo，中文 Noto Sans SC（思源黑体）。圆角统一 8px。
- **标志**：只用白 / 黑两个 SVG 原文件，深底白标、浅底黑标，不改色不变形。
- **内容**：不编造艺人、日期、场地、价格；艺人海报整张放、不裁不压字；AI 图只当氛围示意。
- **现场**：「音乐实物」风格——名片是黑胶封套，标识是歌单，易拉宝是票根 / 歌单 / 正在播放；手环按票种（白 GA · 绿 VIP · 黑 SVIP/卡座），工作人员用工牌，不写 ALL ACCESS。

完整规则在 `skills/sinopop-design/SKILL.md`，给人看的版本在 `docs/`。

## 改规范的顺序

1. 改 `skills/sinopop-design/design-system/tokens/tokens.json`，运行 `python3 skills/sinopop-design/design-system/tokens/build.py`。
2. 规则有变就同步改 `SKILL.md`、`design-system/AGENTS.md`、`chatgpt/PROJECT-INSTRUCTIONS.md`，并在 `docs/CHANGELOG.md` 记一笔。
3. 运行 `bash tools/build-dist.sh` 重新生成 `dist/`，再提交。
4. Figma 源文件（VI 第 82 页、设计规范第 83 页、组件第 30 页、生产预览第 40 页）同步修改后，重新导出 `docs/` 里的两本 PDF。

## 注意

- 这是私有仓库，内容仅供 sinoPOP 内部和合作方使用。
- `design-system/assets/sample-poster-*.png`、`sample-live-photo.jpg` 是排版示例，版权归原作者，不能用于对外发布。
- 所有 AI 效果图和氛围图都不是 sinoPOP 真实活动的照片。
- 亮绿需要荧光专色实物打样；深色底材上的白字白标需要白墨版；二维码都是占位，要换成真码并测试。
