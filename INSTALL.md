# 安装 · 一次装好，以后自动按 sinoPOP 规范产出

仓库：`https://github.com/Sokol13/sinoPOP-Visual-Identity-Skill`（私有）。
先让 Sokol 在仓库 Settings → Collaborators 里邀请你的 GitHub 账号，并在邮件里接受邀请。私有仓库要求你的电脑已经登录 GitHub（装过 GitHub Desktop、`gh auth login` 或者 git 能正常 clone 私有仓库都可以）。

按你用的工具选一段，整段复制粘贴过去就行。

---

## 1. Claude Code（终端 / 桌面版 Code）

把这段发给 Claude Code：

```
帮我安装 sinoPOP 品牌技能。先运行 git ls-remote https://github.com/Sokol13/sinoPOP-Visual-Identity-Skill.git 确认我能访问这个私有仓库，如果提示要登录，就停下来教我用 gh auth login 登录 GitHub；能访问的话依次运行 claude plugin marketplace add Sokol13/sinoPOP-Visual-Identity-Skill 和 claude plugin install sinopop-design@sinopop，然后运行 claude plugin list 确认 sinopop-design@sinopop 是 enabled，最后告诉我：以后更新用 claude plugin marketplace update sinopop，用的时候直接说「按 sinoPOP 规范做……」。
```

也可以自己在会话里输入两条命令：`/plugin marketplace add Sokol13/sinoPOP-Visual-Identity-Skill`，再 `/plugin install sinopop-design@sinopop`。

## 2. Codex（CLI、IDE 插件或 Codex App）

把这段发给 Codex：

```
帮我安装 sinoPOP 品牌规范，全部在我的用户目录下完成：第一步，把私有仓库 https://github.com/Sokol13/sinoPOP-Visual-Identity-Skill.git 克隆到 ~/sinopop-vi，如果文件夹已经存在就进去 git pull；克隆失败提示要登录的话就停下来教我登录 GitHub。第二步，把 ~/sinopop-vi/skills/sinopop-design 整个文件夹复制到 ~/.agents/skills/sinopop-design，已存在就先删掉旧的再复制。第三步，打开 ~/.codex/AGENTS.md（没有就新建），如果里面还没有「sinoPOP」这一段，就在末尾追加这段文字：「## sinoPOP：凡是给 sinoPOP 做的任何东西（网页、公众号、交接文件、名片、手环、工牌、标识、易拉宝、主办方介绍、社媒、印刷），开始前先完整阅读 ~/.agents/skills/sinopop-design/SKILL.md 并严格遵守；模板在同目录的 design-system/，印刷生产文件在 ~/sinopop-vi/production/（先读 START-HERE.md），规范 PDF 在 ~/sinopop-vi/docs/；交付前运行 python3 ~/.agents/skills/sinopop-design/scripts/check_brand.py <产出文件> 并修到没有 ERROR；缺的信息写 [占位]，不要编造。」第四步，列出 ~/.agents/skills/sinopop-design 的内容和 ~/.codex/AGENTS.md 的最后几行给我确认。以后要更新，就把这段话再发一次。
```

Cursor 或其他读 `AGENTS.md` 的编程工具：在项目里用上面第一步克隆仓库，然后把仓库根目录的 `AGENTS.md` 内容加进你项目的 `AGENTS.md`，路径前面加上 `~/sinopop-vi/`。

## 3. Claude App（claude.ai 网页、桌面版、Cowork）

1. 在仓库里下载 `dist/sinopop-design-skill.zip`（网页上点文件 → Download raw file）。
2. 打开 Claude 的设置 → 技能（Skills）页面，上传这个 zip，并保持开启。
3. 以后说「按 sinoPOP 规范做……」就会自动调用。印刷生产文件不在 zip 里，需要时从仓库 `production/` 下载。

仓库更新后，重新下载 zip 再上传一次覆盖。

## 4. ChatGPT（网页 / App）

1. 新建一个 **Project**，名字叫 `sinoPOP`。
2. 项目设置里的 Instructions（指令）：粘贴 `chatgpt/PROJECT-INSTRUCTIONS.md` 的全部内容。
3. 项目文件（Files）：上传 `dist/chatgpt-knowledge/` 里的全部文件，再加上 `docs/sinoPOP-VI-2.1.pdf` 和 `docs/sinoPOP-Design-Standards-2.1.pdf`。
4. 以后所有 sinoPOP 的活都在这个项目里开对话。

也可以用同样的指令和文件做一个自定义 GPT。仓库更新后，把变动的文件重新上传覆盖。

---

## 装好后测一下

随便挑一个工具，发这句：

```
按 sinoPOP 规范，做一张 10 月 24 日演出的网页活动卡片（HTML），艺人、场地、票价都还没定。
```

合格的结果应该是：深色底、日期绿色、层级面是 #181A1F、字体 Archivo + Noto Sans SC、圆角 8px、没定的信息写「待确认」或 [占位]，并且它会自己跑一遍 `check_brand.py`。
