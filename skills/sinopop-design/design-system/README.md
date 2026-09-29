# SinoPOP 设计系统 2.1 定稿（2026.09.28）· sinopop-design-system

给人和 AI 一起用的 SinoPOP 设计规范代码包。人看 Figma 里的两本手册；AI 读这里的文件。

- **VI 规范（给人看）**：Figma 页面「82 · VI规范 2.0」，30 页；定稿 PDF `SinoPOP-VI规范-2.1-定稿.pdf`
- **设计规范（人 + AI）**：Figma 页面「83 · 设计规范 2.0」，10 页；定稿 PDF `SinoPOP-设计规范-2.1-定稿.pdf`；加上这个文件夹
- **印刷生产文件**：`sinopop-music-objects/` 生产包（名片、手环、工牌挂绳、现场标识、易拉宝、主办方介绍），Figma 页面「40 · 音乐实物 GPT 交付」有全部预览
- **组件与模板**：Figma 页面「30 · 组件 2.0」

## 文件夹
```
AGENTS.md                  给编程 AI（Codex / Cursor / Claude Code）的规则入口 —— 先读它
tokens/tokens.json         设计变量源文件（颜色 Dark/Light、字号、间距、圆角）
tokens/tokens.css          由 build.py 生成的 CSS 变量，不要手改
tokens/build.py            python3 tokens/build.py 重新生成 tokens.css
web/sinopop-widgets.css    网页小组件样式
web/widgets-demo.html      所有小组件的示例页（浏览器直接打开）
web/embed/*.html           可直接粘贴进 Wix「嵌入 HTML」的完整小组件
wechat/article-template.html  公众号框架 A · 自办活动（全篇 SinoPOP 视觉）
wechat/article-artist.html    公众号框架 B · 艺人活动（海报主导，借一个海报色）
wechat/*.png               主办条、结尾品牌条、头图、分享封面
handoff/google-docs-guide.md  交接文件在 Google Docs / Sheets 里的样式
assets/                    矢量标志（白 / 黑）与示例图片
```

## 怎么用
- **Claude**：安装技能 `sinopop-design`，然后说「按 SinoPOP 规范做……」。
- **Codex / Cursor**：把整个文件夹放进项目根目录，AI 会先读 `AGENTS.md`。
- **Figma 里的 AI**：直接选中「30 · 组件 2.0」里的组件，说明文字里有用途、禁用和代码对应。
- **Wix 现站**：添加 → 嵌入代码 → 嵌入 HTML，粘贴 `web/embed/` 里的文件，只改里面的文字和链接。
- **公众号**：先选框架（没有特定艺人用 A，有艺人海报用 B）→ 复制对应模板 → B 把借色 `#1863C3` 全文替换成海报色 → 浏览器打开 → 全选复制 → 粘贴到公众号后台。购票卡和客服区两个框架一样，不改。

## 改规范的顺序
先改 `tokens.json` 和 Figma 变量（两边保持一致）→ 运行 build.py → 检查 widgets-demo.html 和 Figma 示例页。

## 注意
- 中文字体统一写作「Noto Sans SC（思源黑体 Source Han Sans SC）」：同一套字形，Google 版叫 Noto Sans SC，Adobe 版叫思源黑体。
- 矢量标志是由已确认的笔刷 PNG（5001×3750）描摹而来，形状未改；正式印刷前请和 PNG 原稿对照确认一次。
- 示例里的艺人、日期、场地都是占位，不是真实活动信息。
- 状态颜色只用「单色 + 绿」；粉色只作活动视觉的点缀，不用在界面、状态和文字上。
- 名片、主办方介绍、现场标识已定稿（VI V24–V29）；早期探索稿留在 Claude 画布「SinoPOP 探索 Explorations」存档。
- 印刷前：亮绿走 SP-GREEN 荧光专色，先打实物样；深色底材上的白字、白标需要印厂做白墨版；二维码换成真码并扫码测试。
- 仍待确认（不在定稿里）：Figma 82 页 X2 绿色标志、X3 给其他主办方的手环配色、粉色是否彻底退出。
