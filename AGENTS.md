# SinoPOP brand kit — instructions for AI agents (Codex, Cursor, Claude Code, any agent)

This repository is SinoPOP's visual identity (VI) and design standards 2.1. Anything made for SinoPOP — web widgets, WeChat 公众号 articles, handoff docs, business cards, wristbands, passes, lanyards, signage, roll-ups, promoter profiles, social or print — must follow it.

## Before you make anything
1. Read `skills/sinopop-design/SKILL.md` in full. It is the complete rule set (hard rules, type sets, credentials, print production, tokens, widget CSS, WeChat modules).
2. Open the matching template instead of rebuilding from memory:
   - tokens: `skills/sinopop-design/design-system/tokens/`
   - web widgets / Wix embeds: `skills/sinopop-design/design-system/web/`
   - WeChat articles (framework A / B): `skills/sinopop-design/design-system/wechat/`
   - handoff docs: `skills/sinopop-design/design-system/handoff/`
   - logos: `skills/sinopop-design/design-system/assets/`
   - print & on-site production files and batch scripts: `production/` (start with `production/START-HERE.md`)
   - brand books for people: `docs/SinoPOP_VI_2.1.pdf`, `docs/SinoPOP_Design_Standards_2.1.pdf`
3. Never invent facts (artists, dates, venues, prices, contacts). Use `[占位]` / `待确认 To be confirmed`.

## Before you hand anything over
Run `python3 skills/sinopop-design/scripts/check_brand.py <files or folder>` and fix every ERROR, then walk the "Before you finish" checklist in SKILL.md.

## Non-negotiables (short version)
- Brand name is always `SinoPOP` (capital S, capital POP); `SINOPOP` only in all-caps settings; lowercase `sinopop` only in URLs, domains and file names.
- Colours only from `tokens.json`: ink `#111318`, surface `#181A1F`, paper `#F7F8F4`, green `#73F64B`, greys `#B7BDC5` `#5A616C` `#3A3F48` `#D8DBD3` (+ documented tints). `#141926` and `#1B1E24` are retired.
- Archivo for Latin and numerals, Noto Sans SC（思源黑体）for Chinese. One radius: 8px.
- Logo: only the two SVG files, white on dark, black on light; never redraw, recolour or let an image model draw it.
- Status = mono + green. Pink is a campaign accent only.
- Artist posters are shown whole — never cropped, never typed over.
- Wristbands by ticket tier (white GA · green VIP · black SVIP/卡座); staff use passes; never write "ALL ACCESS".

## Editing this repo
Change `skills/sinopop-design/design-system/tokens/tokens.json` first, run `python3 skills/sinopop-design/design-system/tokens/build.py`, update SKILL.md if a rule changed, then run `bash tools/build-dist.sh` so the Claude-app zip matches.
