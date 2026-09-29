# sinoPOP 印刷与现场生产文件 · 从这里开始

这个文件夹是 sinoPOP「音乐实物」系列的全部生产文件，由 GPT/Codex 分三次交付，已经合并好。视觉规则以 `../docs/sinoPOP-VI-2.1.pdf` 的 V24–V29 页为准；文字规则以 `../skills/sinopop-design/SKILL.md` 为准。

## 哪些是定稿，哪些是存档

| 文件夹 | 状态 | 内容 |
|---|---|---|
| `task-04-card-final` | **定稿** | 名片 · 黑胶封套（曲目号 A1）：封套 + 内卡 + 刀模，`batch_staff.py` 按 `staff.csv` 批量出内卡 |
| `task-05-wristbands` | **定稿** | 三档 Tyvek 手环：白 GA（早鸟同档）· 绿 VIP · 黑 SVIP/卡座；A3 拼版、按档流水号批量脚本 |
| `task-06-passes-lanyards` | **定稿** | 6 种身份工牌（1–4 通行区域）+ 4 款挂绳；按 `passes.csv` 批量出工牌 |
| `task-07-signage` | **定稿** | 10 款「歌单」现场标识 + SignFamily 总览，字高记录 |
| `task-08-rollups` | **定稿** | 3 款易拉宝 850 × 2000 mm：票根 / 歌单 / 正在播放 |
| `task-09-profile` | **定稿** | 主办方介绍竖版：A4、Letter 各 6 页 + 手机 1080 × 1920 × 6 |
| `task-01-cards` | 存档 | 第一轮 6 个名片方向，只选了 `03-vinyl`，定稿在 task-04 |
| `task-02-onsite` | 效果图 | 现场 AI 效果图（示意，不是真实活动照片）；`onsite-04-kit.png` 为第二轮新版 |
| `task-03-profile` | 氛围图 | 主办方介绍用的 AI 氛围图（仅氛围，不可当作真实活动照片） |

## 每个物料的文件怎么用

- `*-print.pdf` → 交给印厂。CMYK + 专色 `SP-GREEN`（亮绿走荧光专色，需实物打样），带出血、裁切线、TrimBox / BleedBox。
- `*-rgb.pdf` → 屏幕看稿、打样对色用。
- `*-technical.pdf` → 刀模、打孔、折线，单独给印厂，不印在成品上。
- `*.svg` → 可编辑源文件（文字没转曲）。改字后用脚本重新生成，别手工描。
- `*-preview.png` → 预览。
- 深色底材（黑卡、深色 Tyvek）上的白字白标需要印厂做白墨版。
- 二维码框都是空的，换成真码并扫码测试后才能生产。
- 所有姓名、电话、艺人、日期、场地、价格都是 `[占位]`，填真实信息后再批量输出。

## 重新生成

```bash
pip install -r requirements.txt
python build_card_final.py      # 名片
python build_credentials.py     # 手环、工牌、挂绳
python build_signage.py         # 标识
python build_rollups.py         # 易拉宝
python task-09-profile/build-profile.py   # 主办方介绍
python qa_round2.py             # 复查
```

各文件夹里的 README 有批量输入格式和命令。颜色来自 `production-tokens.json`，大面积深色底 = 层级面 `#181A1F`（印刷 CMYK C22.6 M16.1 Y0 K87.8），墨黑 `#111318`。

## 变更记录

`README.md`（第一轮）· `README-round2.md` / `CHANGES-round2.md`（第二轮）· `CHANGES-surface.md`（层级面改色）· `qa/`（全部 QA 证据）。
