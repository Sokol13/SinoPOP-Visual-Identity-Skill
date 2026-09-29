---
name: "sinopop-design"
description: "Use whenever making anything for SinoPOP (the promoter brand) — web widgets, WeChat 公众号 articles, handoff docs (事实卡、艺人交接单、报价), letterheads, business cards, wristbands, passes & lanyards, on-site signage, roll-ups, promoter profile, print files or any on-brand visual/code — so it follows VI & design standards 2.1 (final)."
---

# SinoPOP design system 2.1 (final, 2026-09-28)
Follow these rules exactly. If a request conflicts with a hard rule, say so and follow the rule. Never invent event facts.
SinoPOP is a music & live-culture **promoter** rooted in Chinese youth music, bringing live shows to young audiences abroad. You are building one of: **web widgets**, **WeChat Official Account articles (公众号)**, **handoff documents (交接文件)**, or **on-site / print pieces**. Everything essential is in this skill. Do not invent a new style.

Source of truth: GitHub repo `Sokol13/SinoPOP-Visual-Identity-Skill` (private). Paths below starting with `design-system/` and `scripts/` are inside this skill folder. `docs/` and `production/` are at the repo root (two levels up from this file when the repo is cloned); if they are not on disk, tell the person they live in that repo.

## How to work (every time)
1. Pick the output type and open the matching file from the table below — copy the template, don't rebuild it from memory.
2. Use only token colours, the two typefaces, one 8px radius, and the real logo files.
3. Leave every unknown fact as `[占位]` / `待确认 To be confirmed`.
4. Before handing over any HTML / CSS / SVG / code, run `python3 scripts/check_brand.py <your files>` and fix every ERROR (it catches off-palette colours, retired colours and forbidden wording). Then walk the "Before you finish" list.
5. If the request conflicts with these rules, say which rule and follow the rule.

## Files
| Need | Use |
|---|---|
| Colors, type, spacing, radius | `design-system/tokens/tokens.json` (source) → `design-system/tokens/tokens.css` (run `python3 design-system/tokens/build.py` after editing) |
| Web widgets (Wix embed or V2 site) | `design-system/web/sinopop-widgets.css` + `design-system/tokens/tokens.css`; examples `design-system/web/widgets-demo.html`, `design-system/web/lang-switch-demo.html`; paste-ready Wix embeds in `design-system/web/embed/` |
| WeChat article | Framework A (self-run, no specific artist): `design-system/wechat/article-template.html` · Framework B (artist-led, poster first): `design-system/wechat/article-artist.html` — inline styles only; header / host-bar / brand-bar / cover PNGs in `design-system/wechat/` |
| Handoff doc | Figma page `30 · 组件 2.0` → `Template 2.1/…`; Google Docs: `design-system/handoff/google-docs-guide.md` |
| Logo | `design-system/assets/sinopop-logo-white.svg`, `design-system/assets/sinopop-logo-black.svg` (vector trace of the approved brush PNG) |
| Brand books (for people) | `docs/SinoPOP_VI_2.1.pdf` (30 pages) · `docs/SinoPOP_Design_Standards_2.1.pdf` (10 pages) · `docs/CHANGELOG.md` |
| Print / on-site | VI pages V24–V29 in `docs/SinoPOP_VI_2.1.pdf`. Production files + batch scripts: `production/` (`task-04-card-final` … `task-09-profile`; read `production/START-HERE.md` first; `task-01`–`task-03` are round-1 explorations, only `03-vinyl` was chosen and its final is `task-04`). Rebuild with the scripts (`pip install -r production/requirements.txt`), never redraw by hand |
| Explorations (archive) | Figma 82 frames X1 / X4 surface tint (X4-C `#181A1F` adopted; ink blue `#141926` retired) · X2 green logo · X3 wristband colours for other promoters — not approved, don't use unless the user says so |
| Figma | File `oQLs4rdfXbgzhLE0XDpTri`. Variables: `SinoPOP / Primitives`, `SinoPOP / Color` (modes Dark, Light), `SinoPOP / Dimensions`. Each variable's WEB code syntax = the CSS variable. Each component description lists USE / DON'T / PROPS / CODE / TOKENS. |

## Hard rules (never break)
1. Colors come only from tokens. Never add a hex value that isn't in `tokens.json`. Only exception: the one borrowed poster accent in WeChat framework B (see WeChat).
2. One radius: `var(--sp-radius)` = 8px on every component at every size. Never scale radius with size. Images and full-bleed media: 0.
3. Font stack: `var(--sp-font)` = `Archivo, "Noto Sans SC", …` — Latin letters and numerals render in Archivo, Chinese in Noto Sans SC. WeChat: system font only (no web fonts).
   Naming: always write the Chinese face as **Noto Sans SC（思源黑体 Source Han Sans SC）** — same design; Google ships it as Noto Sans SC, Adobe as Source Han Sans SC. Never mix both installs in one file.
4. **Website = language switch, not mixing.** Each page is one language: set `lang="zh-CN"` or `lang="en"` on `<html>` (or on `.sp-root`) and the whole type set switches (sizes, leading, tracking, label case). Do not print the second language underneath. Localize formats: zh `10月24日 周六 19:30`, en `Sat, Oct 24 · 7:30 PM`, prices `USD 45`.
   Mixed bilingual layouts (Chinese first, English second) are only for WeChat, handoff docs, social and print; there use `10.24 SAT 19:30`. One space between Chinese and Latin/numerals.
5. Status = **mono + green**. Green fill = act now (On sale, Tonight); green outline = soon (Coming soon, Waitlist); paper fill = attention (Rescheduled, Postponed) — ink on light backgrounds; paper outline = Selling fast; grey fill = Sold out; grey outline = Ended; paper outline + × = Cancelled. No other hues for status. Pink `#FF89B8` is a campaign accent only (social/print art) — never UI, status or text.
6. On light backgrounds never use `#73F64B` as text — use `--sp-color-accent-text` (green 700 `#286C2A`). Emphasis text is `--sp-color-emphasis-text` (paper on dark, ink on light).
7. Event info order is fixed: date (green) → Chinese title → English title → city · venue → status tag → action.
8. **Never invent facts** (dates, venues, prices, artists, contacts, fees). If missing, write `待确认 To be confirmed` (web: `.sp-facts__todo`; Figma: `Web/FactRow State=TBC`). AI-generated photos are mood images only — never present them as past SinoPOP shows.
9. Artist posters are artwork: show whole (`object-fit: contain`), never crop, never type over them. Show photos may be cropped (`cover`) if the performer and action survive.
10. Logo: black or white version only, transparent background. Never redraw, retype, recolor, outline, add effects, box, stretch or rotate. White on dark, black on light. Never let an image model draw it — leave a blank area and place the real file.
11. Status must be written in words (bilingual). Color only supports it. Every status notice says what happens next.
12. In mixed-bilingual pieces: Chinese first, English second, same order throughout.
13. **Brand name is written `SinoPOP`** — capital S, capital POP — in every language and every file. All-caps settings may use `SINOPOP`. Lowercase `sinopop` only in URLs, domains (`sinopop.us`), file names and code identifiers. Never `sinoPOP`, `Sinopop` or `SinoPop`.

## Type sets (tokens.json → type.zh / type.en)
| role | zh — Noto Sans SC（思源黑体） desktop/mobile · leading · tracking | en (Archivo) |
|---|---|---|
| display | 88/48 · 1.15 · +0.02em · 900 | 96/56 · 1.0 · −0.02em · 800 |
| h1 | 56/34 · 1.25 · +0.02em | 60/38 · 1.05 · −0.015em |
| h2 | 36/26 · 1.3 · +0.02em | 40/28 · 1.1 · −0.01em |
| h3 | 24/20 · 1.45 · +0.02em | 26/21 · 1.25 · 0 |
| body | 17/16 · 1.8 · +0.03em · measure 36em | 17/16 · 1.55 · 0 · measure 66ch |
| caption | 14/13 · 1.65 · +0.03em | 14/13 · 1.45 · 0 |
| label | 13/12 · 1.4 · +0.12em · no caps | 12/12 · 1.3 · +0.08em · UPPERCASE |
Figma text styles: `SinoPOP 2.1 / zh / …` and `SinoPOP 2.1 / en / …`. Demo: `web/lang-switch-demo.html`.

## Themes
- Web widgets: Dark (default). Add `data-sp-theme="light"` on a wrapper for light sections.
- WeChat article body and handoff docs: Light. Brand dark lives in the header image (framework A), the host bar (framework B) and the brand bar in the service footer.
- In Figma, set the outer frame's `SinoPOP / Color` mode to Light; bound components switch automatically.

## Web widgets
- Wrap everything in `<div class="sp-root">`. Classes: `.sp-btn[--secondary|--ghost][--s]`, `.sp-tag--soon|--waitlist|--on-sale|--tonight|--selling-fast|--changed|--postponed|--sold-out|--ended|--cancelled`, `.sp-event-card[--row]`, `.sp-event-grid`, `.sp-facts` / `.sp-facts__row` / `.sp-facts__todo`, `.sp-notice[--attention|--critical]` (status block + message + next step + updated time), `.sp-section-head`.
- Wix: Add → Embed Code → Embed HTML → paste a file from `web/embed/` and edit only the markup.
- V2 site: import `tokens.css` + `sinopop-widgets.css`; keep the class names (port to components 1:1 if using React).
- Buttons ≥ 48px tall (`--sp-control-m`); one primary button per area; grid collapses to one column on phones.

## WeChat (公众号)
- Inline styles only. No `<style>`, no scripts, no web fonts, no external CSS. Deliver HTML; the person opens it in a browser, copies all, pastes into the WeChat editor. Check at 375 px and in dark mode.
- **Pick a framework first.** No specific artist (party, theme night) → **A** `article-template.html`: full SinoPOP look (dark header image with white logo, green section numbers, ink key-point bar). Artist show with a poster → **B** `article-artist.html`: poster-led middle, SinoPOP at top and bottom.
- **Three fixed zones — identical in A and B, never restyled:**
  - F1 Host bar (B only, first thing in the article): `hostbar-dark-1080.png` / `hostbar-light-1080.png` (match the poster's lightness). Figma `WX/HostBar`.
  - F2 Ticket card (in the 购票 section): must be text — date, title, venue, price, on-sale time, ink CTA 「点击「阅读原文」购票」, 主办 SinoPOP. Figma `WX/TicketCard`.
  - F3 Service footer (last): ticket instructions + customer-service QR (text) + `brandbar-1080.png`. Figma `WX/ServiceFooter`.
- **Borrowed accent (B only):** take ONE saturated colour from the poster; white text on it must reach ≥ 4.5:1, else darken it. It appears in exactly four places: section-number chip, divider, key-point left bar, ticket-card top line. Body text stays `#111318`; backgrounds stay white or paper `#F7F8F4`; notices (M09) stay mono. In the HTML it is the single hex `#1863C3` — find and replace it.
- **Poster:** full width, whole image, never cropped, never typed over, placed directly under the host bar.
- **Long image vs text:** visual parts (header image, poster, line-up art, footer brand bar) may be images, exported 1080 wide with body type ≥ 32 px. Ticket info and rules are always copyable text. Never publish a ticketing article as one long image only.
- Modules: M01 header image (A) · M02 lead · M04 section title · M05 paragraph (16 px / 1.8) · M06 key point (paper + ink/accent bar, max 2) · M07 image + caption with credit · M08 quote · M09 notice (mono: ink outline + ink label, max 1, says what happens next) · M10 divider · then F2, F3. Share cover `cover-900x383.png`: title and date inside the centre 383×383 square.

## Handoff docs (交接文件)
- Templates in Figma page `30 · 组件 2.0`: `Template 2.1/A4 事实卡`, `A4 艺人交接单 p1 + p2`, `A4 报价单`; spec board `Spec · 交接文件规格`.
- A4 794×1123 (PDF), Light mode, side margins 56 (content 682 wide).
- Page 1: `Doc/Header` dark band — white logo 64×48 top-left (56 from left, 40 from top); right-aligned: type (Archivo SemiBold 12, caps, green) → title (Noto Bold 24) → `版本 v01 · 更新 YYYY.MM.DD · 编号`.
- Page 2+: `Doc/HeaderCont` — black logo 32×24 top-left, doc title + `续 Continued · v01` right, 1px divider.
- Every page: `Doc/Footer` — left `SinoPOP · 内部资料 Internal`, center file name, right page `1 / 2` (Archivo).
- Body: `Doc/SectionTitle` → `Web/FactRow` (label 14 #5A616C, value 16 Medium #111318, TBC in muted grey `--sp-color-muted`) / `Doc/ScheduleRow` / `Doc/QuoteRow` (numbers right-aligned, USD) / `Doc/CheckItem` / `Doc/SignBlock`.
- WeChat long image: lay out at 450 wide, export ×2.4 = 1080 wide PNG.
- File name: `SinoPOP_{类型}_{艺人}_{城市}_v01_YYYYMMDD.pdf`. Bump the version on every change and update the header.

## Office paper (letterhead, proposals, quotes)
Logo is small: header logo ≤ 32×24 (continuation style) or none. Brand presence comes from `Doc/Watermark`: black logo at 5% opacity, 560×560, centred on A4 / Letter, straight or tilted 20°, under the text; never green, never above 8%, never on dark pages.

## On-site & print personality: music objects
Every physical piece borrows from a real music object — ticket, setlist, album cover / tracklist, a player's "now playing" screen, a vinyl sleeve. Big Archivo ExtraBold numbers, perforated stubs, strips of green gaffer tape. Still only the flat palette below.
- **Signage = Setlist.** Every stop is a track: 01 入场 DOORS · 02 验票 CHECK-IN / 排队起点 · 03 寄存 COAT CHECK · 04 酒水 · 周边 BAR · B-SIDE · 05 演出 THE SHOW / 站这里拍 PHOTO SPOT · — 中场 · 洗手间 INTERMISSION · 06 返场 · 出口 ENCORE · WAY OUT. The functional Chinese word is always the biggest line; English in light grey caps; one short playful line allowed (轻装上阵). Entrance A-frame = a ticket with a tear line. Sign tones: ink = wayfinding, paper + thick ink frame = notice (ID, rules), green only for arrows. Legal EXIT signs are the venue's — never make or cover them.
- **Roll-ups 850 × 2000 mm:** A Ticket (welcome, green stub with QR) · B Setlist (paper setlist taped on ink, row 05 green, per-show sticker strip) · C Now Playing (artist poster whole in an empty album frame, player bar below).
- **Promoter profile: vertical by default** — A4 / Letter 6 pages (cover = album cover, contents = tracklist, 01 who we are, 02 what we do: 活动主办与执行 · 宣传推广 · 售票, 03 past shows = real photos only, 04 how we work + contact) and 9:16 phone × 6 with a NOW PLAYING cover. Landscape only when presenting on a screen.
- **Business card = vinyl sleeve (final, VI V24).** Ink sleeve with round die-cut window showing a green record label (SIDE A · SinoPOP), track number `A1`, white logo; name and contacts only on the pull-out insert.

## On-site credentials (wristbands, passes, lanyards)
- Wristbands are for the audience only and follow the ticket tier: white/paper = GA (early bird is the same tier), green = VIP, ink black = SVIP / table (卡座, top tier). Tier is always written in words; every band carries a serial number; logo on the band (black on white/green, white on black).
- Staff, artists and guests never wear wristbands; they use passes. No "ALL ACCESS" wording anywhere.
- Passes (90 × 130 mm) show role + numbered access zones (1 floor · 2 backstage · 3 stage · 4 green room). Roles: STAFF (green band), ARTIST (ink band, thick green outline), ARTIST TEAM (ink band, thin green outline), GUEST (paper band), PRESS (grey band), PRODUCTION (ink band, grey outline).
- Lanyards show which side you belong to: green = SinoPOP team, black with green print = artist side (artist + artist team), white = guests, grey = press and production.
- For other promoters: tiers are always light → brand accent → dark; one accent per band; text contrast ≥ 4.5:1 (Figma page 82, frame X3).

## Print & on-site production
- Flat colours in print: ink `#111318`, surface `#181A1F` (ink lifted 3%, same hue — every large dark panel), paper `#F7F8F4`, green `#73F64B`, greys `#B7BDC5` `#5A616C` `#3A3F48` `#D8DBD3`. Nothing else except photos.
- Every printed item ships as: `*-rgb.pdf` (screen proof) + `*-print.pdf` (CMYK, green on its own spot plate named `SP-GREEN`, no ink brand number) + `*-technical.pdf` (die-cut, holes, folds only — never on the printed face). Bleed 3 mm (0.125 in for US sizes, 5 mm roll-ups), crop marks, TrimBox/BleedBox, fonts embedded, output at 100%.
- Green is fluorescent-spot territory: always ask for a physical proof. White text or logo on dark stock (black board, dark Tyvek) needs a white-ink plate from the printer.
- Type: Archivo for Latin/numerals; Noto Sans SC Heavy for big Chinese titles, and for small Chinese match the weight of the Latin on the same line (Regular / Medium / Bold). Minimum 7 pt printed. Far-reading signs follow the height table in the signage package.
- Sizes: card sleeve 88.9 × 50.8 mm folded (insert 86.9 × 48.8) · wristband 250 × 25 mm, 38 mm adhesive tab with 「撕开即失效」+ serial · pass 90 × 130 mm · lanyard 20 × 900 mm, double-sided repeat · hanging sign 1200 × 300 · entrance A-frame 600 × 850 · rules board 600 × 900 · floor sticker Ø 600 · wall A3 · pillar Letter · table tent A5 · roll-up 850 × 2000 mm with the bottom 150 mm empty · profile A4 / Letter 6 pages + phone 1080 × 1920 × 6.
- Business card = vinyl sleeve: sleeve number is the track number `A1`, contact details only on the insert. Batch per person from `staff.csv`.
- Wristband serials: each tier has its own number range (GA 000001…, VIP 100001…, SVIP 200001…); never overlap, never skip.
- Signage = setlist skin: every point has a track number, the function word is the biggest thing, English is light-grey caps, green is only for arrows, one message per sign, the arrow sits on the side it points to, no event name or date on wayfinding.
- Roll-up C and any artist use: the artist poster goes in whole — no cropping, no type over it. Never generate an artist poster.
- Promoter profile: only the confirmed line 「从华语青年音乐与文化出发，把现场带给海外的年轻观众。」 is real copy; everything else stays `[占位]` until the person supplies it. Past-show pages need real event photos with photographer credit — AI images are mood only and never presented as SinoPOP events.
- QR boxes are placeholders; replace with a real code and test-scan before print.

## Voice
Bold but clear. Lead with date, venue, price, next step. No unverifiable superlatives (史上最强 / the biggest ever). No "stay tuned" without a date or next step.

## Before you finish, check
Contrast ≥ 4.5:1 for text · no TBC left in public versions · viewed at 375px wide · cover safe area holds title and date · correct logo version · version/date updated · image source & rights noted.

## Figma (file key `oQLs4rdfXbgzhLE0XDpTri`)
Pages: `82 · VI规范 2.0` (brand book, 30 frames V01–V30 92:10; V24 card 142:464 · V25 profile 142:520 · V26 signage 99:72 · V27 roll-ups 142:576 · V28 wristbands 142:632 · V29 passes & lanyards 142:688) · `83 · 设计规范 2.0` (standards, 10 frames) · `30 · 组件 2.0` (components & templates) · `40 · 音乐实物 GPT 交付` (production previews and editable card vectors). `80`/`81` are 1.0 archives — never edit.
- Web: Button 102:25 · StatusTag 102:36 (10 variants, fixed labels) · SectionHead 102:37 · FactRow 102:47 · Notice 102:64 (Tone=Info/Attention/Critical) · EventCard 103:39
- WeChat: HostBar 125:374 (Tone=Dark/Light) · TicketCard 125:375 · ServiceFooter 125:396 · SectionTitle 103:42 · KeyPoint 103:47 · Cover 900×383 103:68. Mockups: framework A 127:368 · B 127:431 · rules board 128:447
- Handoff: Doc/Header 104:28 · Doc/HeaderCont 113:183 · Doc/Footer 104:52 · Doc/QuoteRow 113:213 · Doc/CheckItem 113:214 · Doc/SignBlock 113:217 · Doc/Watermark 123:352 (Straight/Tilted, black logo 5%). Templates 2.1: fact sheet 114:471 · artist handoff 114:544 + 114:623 · quote 114:693 · spec board 115:407 · letterheads A4 123:353 / 123:369 · Letter 123:385 / 123:401
- Logo: white 91:5479 · black 91:5481
Build from instances; set the outer frame's `SinoPOP / Color` mode; set every component property explicitly on new instances. Text styles: `SinoPOP 2.1 / zh|en / display|h1|h2|h3|body|caption|label`.

## tokens.css (paste into any web output)
```css
/* Generated from tokens.json — do not edit by hand. */
:root, .sp-root {
  --sp-ink: #111318;
  --sp-surface: #181A1F;
  --sp-line: #626A76;
  --sp-line-subtle: #3A3F48;
  --sp-muted: #B7BDC5;
  --sp-paper: #F7F8F4;
  --sp-white: #FFFFFF;
  --sp-sub: #5A616C;
  --sp-line-light: #D8DBD3;
  --sp-green: #73F64B;
  --sp-pink: #FF89B8;
  --sp-green-950: #102816;
  --sp-green-800: #214C24;
  --sp-green-700: #286C2A;
  --sp-green-600: #3EAE32;
  --sp-green-300: #B1FAA0;
  --sp-green-100: #E7FCE1;
  --sp-pink-950: #351D2A;
  --sp-pink-800: #6B2849;
  --sp-pink-700: #A63264;
  --sp-pink-600: #D9578B;
  --sp-pink-300: #FFC0D9;
  --sp-pink-100: #FFF0F6;
  --sp-green-hover: #8AFF62;
  --sp-error: #FF8E8E;
  --sp-error-dark: #B42318;
  --sp-space-4: 4px;
  --sp-space-8: 8px;
  --sp-space-12: 12px;
  --sp-space-16: 16px;
  --sp-space-20: 20px;
  --sp-space-24: 24px;
  --sp-space-32: 32px;
  --sp-space-48: 48px;
  --sp-space-64: 64px;
  --sp-space-80: 80px;
  --sp-radius: 8px;
  --sp-control-m: 48px;
  --sp-control-s: 36px;
}
:root, .sp-root, [data-sp-theme="dark"] {
  --sp-color-bg: var(--sp-ink);
  --sp-color-surface: var(--sp-surface);
  --sp-color-text: var(--sp-paper);
  --sp-color-muted: var(--sp-muted);
  --sp-color-border: var(--sp-line);
  --sp-color-divider: var(--sp-line-subtle);
  --sp-color-accent: var(--sp-green);
  --sp-color-on-accent: var(--sp-ink);
  --sp-color-accent-text: var(--sp-green);
  --sp-color-emphasis: var(--sp-paper);
  --sp-color-on-emphasis: var(--sp-ink);
  --sp-color-emphasis-text: var(--sp-paper);
  --sp-color-accent-hover: var(--sp-green-hover);
  --sp-color-error: var(--sp-error);
  --sp-color-final: var(--sp-line-subtle);
  --sp-color-on-final: var(--sp-muted);
}
[data-sp-theme="light"] {
  --sp-color-bg: var(--sp-white);
  --sp-color-surface: var(--sp-paper);
  --sp-color-text: var(--sp-ink);
  --sp-color-muted: var(--sp-sub);
  --sp-color-border: var(--sp-sub);
  --sp-color-divider: var(--sp-line-light);
  --sp-color-accent: var(--sp-green);
  --sp-color-on-accent: var(--sp-ink);
  --sp-color-accent-text: var(--sp-green-700);
  --sp-color-emphasis: var(--sp-ink);
  --sp-color-on-emphasis: var(--sp-white);
  --sp-color-emphasis-text: var(--sp-ink);
  --sp-color-accent-hover: var(--sp-green-hover);
  --sp-color-error: var(--sp-error-dark);
  --sp-color-final: var(--sp-line-light);
  --sp-color-on-final: var(--sp-sub);
}
/* Typesetting: Chinese is the default; any element with lang="en" switches to the English set. */
:root, [lang|="zh"] {
  --sp-font: Archivo, "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
  --sp-measure: 36em;
  --sp-type-display: 88px;
  --sp-type-display-lh: 1.15;
  --sp-type-display-wt: 900;
  --sp-type-display-ls: 0.02em;
  --sp-type-h1: 56px;
  --sp-type-h1-lh: 1.25;
  --sp-type-h1-wt: 700;
  --sp-type-h1-ls: 0.02em;
  --sp-type-h2: 36px;
  --sp-type-h2-lh: 1.3;
  --sp-type-h2-wt: 700;
  --sp-type-h2-ls: 0.02em;
  --sp-type-h3: 24px;
  --sp-type-h3-lh: 1.45;
  --sp-type-h3-wt: 500;
  --sp-type-h3-ls: 0.02em;
  --sp-type-body: 17px;
  --sp-type-body-lh: 1.8;
  --sp-type-body-wt: 400;
  --sp-type-body-ls: 0.03em;
  --sp-type-caption: 14px;
  --sp-type-caption-lh: 1.65;
  --sp-type-caption-wt: 400;
  --sp-type-caption-ls: 0.03em;
  --sp-type-label: 13px;
  --sp-type-label-lh: 1.4;
  --sp-type-label-wt: 500;
  --sp-type-label-ls: 0.12em;
  --sp-type-label-case: none;
}
[lang|="en"] {
  --sp-font: Archivo, "Noto Sans SC", sans-serif;
  --sp-measure: 66ch;
  --sp-type-display: 96px;
  --sp-type-display-lh: 1.0;
  --sp-type-display-wt: 800;
  --sp-type-display-ls: -0.02em;
  --sp-type-h1: 60px;
  --sp-type-h1-lh: 1.05;
  --sp-type-h1-wt: 700;
  --sp-type-h1-ls: -0.015em;
  --sp-type-h2: 40px;
  --sp-type-h2-lh: 1.1;
  --sp-type-h2-wt: 700;
  --sp-type-h2-ls: -0.01em;
  --sp-type-h3: 26px;
  --sp-type-h3-lh: 1.25;
  --sp-type-h3-wt: 600;
  --sp-type-h3-ls: 0em;
  --sp-type-body: 17px;
  --sp-type-body-lh: 1.55;
  --sp-type-body-wt: 400;
  --sp-type-body-ls: 0em;
  --sp-type-caption: 14px;
  --sp-type-caption-lh: 1.45;
  --sp-type-caption-wt: 400;
  --sp-type-caption-ls: 0em;
  --sp-type-label: 12px;
  --sp-type-label-lh: 1.3;
  --sp-type-label-wt: 600;
  --sp-type-label-ls: 0.08em;
  --sp-type-label-case: uppercase;
}
@media (max-width: 640px) {
  :root, [lang|="zh"] {
    --sp-type-display: 48px;
    --sp-type-h1: 34px;
    --sp-type-h2: 26px;
    --sp-type-h3: 20px;
    --sp-type-body: 16px;
    --sp-type-caption: 13px;
    --sp-type-label: 12px;
  }
  [lang|="en"] {
    --sp-type-display: 56px;
    --sp-type-h1: 38px;
    --sp-type-h2: 28px;
    --sp-type-h3: 21px;
    --sp-type-body: 16px;
    --sp-type-caption: 13px;
    --sp-type-label: 12px;
  }
}
```

## sinopop-widgets.css
```css
/* SinoPOP web widgets v2.1 — requires tokens.css (or the inlined variables in embed/*.html).
   Rules: one radius (--sp-radius, 8px) at every size; status = mono + green (green = act, paper/ink = attention, grey = over; no pink in UI);
   Latin + numerals render in Archivo via the font stack. Dark by default; add data-sp-theme="light" to any wrapper.
   Language: the website shows ONE language per page. Put lang="zh-CN" or lang="en" on <html> or on .sp-root —
   type sizes, leading, tracking and label case switch automatically (see tokens.css). */

.sp-root { font-family: var(--sp-font); color: var(--sp-color-text); background: var(--sp-color-bg);
  font-size: var(--sp-type-body); line-height: var(--sp-type-body-lh); letter-spacing: var(--sp-type-body-ls); -webkit-font-smoothing: antialiased; }
.sp-root [lang] { font-family: var(--sp-font); font-size: var(--sp-type-body); line-height: var(--sp-type-body-lh); letter-spacing: var(--sp-type-body-ls); }
.sp-root p { max-width: var(--sp-measure); }
.sp-root *, .sp-root *::before, .sp-root *::after { box-sizing: border-box; }
.sp-root img { display: block; max-width: 100%; }

/* ---------- Text roles */
.sp-label { font-size: var(--sp-type-label); font-weight: var(--sp-type-label-wt); letter-spacing: var(--sp-type-label-ls); text-transform: var(--sp-type-label-case, uppercase); color: var(--sp-color-accent-text); }
.sp-h1 { font-size: var(--sp-type-h1); line-height: var(--sp-type-h1-lh); font-weight: var(--sp-type-h1-wt); letter-spacing: var(--sp-type-h1-ls); margin: 0; }
.sp-h2 { font-size: var(--sp-type-h2); line-height: var(--sp-type-h2-lh); font-weight: var(--sp-type-h2-wt); letter-spacing: var(--sp-type-h2-ls); margin: 0; }
.sp-h3 { font-size: var(--sp-type-h3); line-height: var(--sp-type-h3-lh); font-weight: var(--sp-type-h3-wt); letter-spacing: var(--sp-type-h3-ls); margin: 0; }
.sp-muted { color: var(--sp-color-muted); }
.sp-caption { font-size: var(--sp-type-caption); line-height: var(--sp-type-caption-lh); color: var(--sp-color-muted); }

/* ---------- Section head: label → CN title → EN title */
.sp-section-head { display: grid; gap: var(--sp-space-8); margin-bottom: var(--sp-space-32); }
.sp-section-head .sp-en { /* mixed-bilingual mode only */ font-size: var(--sp-type-h3); line-height: 1.3; color: var(--sp-color-muted); margin: 0; font-weight: 400; }

/* ---------- Button */
.sp-btn { display: inline-flex; align-items: center; justify-content: center; gap: var(--sp-space-8);
  min-height: var(--sp-control-m); padding: 0 var(--sp-space-24); border-radius: var(--sp-radius);
  font: 600 16px/1 var(--sp-font); text-decoration: none; white-space: nowrap; flex-shrink: 0; cursor: pointer; border: 1px solid transparent;
  background: var(--sp-color-accent); color: var(--sp-color-on-accent); transition: filter .15s; }
.sp-btn:hover { filter: brightness(1.08); }
.sp-btn:focus-visible { outline: 2px solid var(--sp-color-accent); outline-offset: 2px; }
.sp-btn--secondary { background: transparent; color: var(--sp-color-text); border-color: var(--sp-color-border); }
.sp-btn--ghost { background: transparent; color: var(--sp-color-accent-text); padding: 0 var(--sp-space-8); }
.sp-btn--s { min-height: var(--sp-control-s); padding: 0 var(--sp-space-16); font-size: 14px; }
.sp-btn[aria-disabled="true"] { background: var(--sp-color-divider); color: var(--sp-color-muted); pointer-events: none; }

/* ---------- Status tag — Mono + Green. Always text; color only supports it.
   green fill = act · green outline = soon · paper fill = attention · outline = selling fast · grey = final · outline + × = cancelled */
.sp-tag { display: inline-flex; align-items: center; gap: 6px; height: 28px; padding: 0 var(--sp-space-12); border-radius: var(--sp-radius);
  font: 600 12px/1 var(--sp-font); letter-spacing: .06em; text-transform: uppercase; white-space: nowrap; border: 1px solid transparent; }
.sp-tag::before { content: ""; width: 6px; height: 6px; border-radius: 3px; background: currentColor; }
.sp-tag--on-sale, .sp-tag--tonight { background: var(--sp-color-accent); color: var(--sp-color-on-accent); }
.sp-tag--soon, .sp-tag--waitlist { color: var(--sp-color-accent-text); border-color: currentColor; }
.sp-tag--changed, .sp-tag--postponed { background: var(--sp-color-emphasis); color: var(--sp-color-on-emphasis); }
.sp-tag--selling-fast { color: var(--sp-color-emphasis-text); border-color: currentColor; }
.sp-tag--sold-out { background: var(--sp-color-final); color: var(--sp-color-on-final); }
.sp-tag--ended { color: var(--sp-color-muted); border-color: var(--sp-color-border); }
.sp-tag--cancelled { color: var(--sp-color-emphasis-text); border: 1.5px solid currentColor; }
.sp-tag--cancelled::before { content: "\00D7"; width: auto; height: auto; background: none; font-size: 13px; }

/* ---------- Event card: date (green) → title → EN title → venue → tag + action */
.sp-event-card { display: flex; flex-direction: column; background: var(--sp-color-surface); border-radius: var(--sp-radius); overflow: hidden; }
.sp-event-card__media { aspect-ratio: 4 / 5; background: var(--sp-ink); }
.sp-event-card__media img { width: 100%; height: 100%; object-fit: cover; }
.sp-event-card__media--poster img { object-fit: contain; }   /* artist posters: never crop */
.sp-event-card__body { display: flex; flex-direction: column; gap: var(--sp-space-4); padding: var(--sp-space-20); flex: 1; }
.sp-event-card__date { font-weight: 700; font-size: 18px; color: var(--sp-color-accent-text); }
.sp-event-card__title { font-weight: 700; font-size: var(--sp-type-h3); line-height: 1.3; letter-spacing: var(--sp-type-h3-ls); margin: var(--sp-space-4) 0 0; }
.sp-event-card__title-en { /* mixed-bilingual mode only; omit on single-language pages */ font-weight: 700; font-size: 15px; line-height: 1.3; color: var(--sp-color-muted); margin: 0; text-transform: uppercase; letter-spacing: .02em; }
.sp-event-card__venue { font-size: 14px; color: var(--sp-color-muted); margin-top: var(--sp-space-8); }
.sp-event-card__foot { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: var(--sp-space-12); margin-top: auto; padding-top: var(--sp-space-16); }
.sp-event-card--row { flex-direction: row; }
.sp-event-card--row .sp-event-card__media { position: relative; width: 38%; flex: none; aspect-ratio: auto; min-height: 240px; }
.sp-event-card--row .sp-event-card__media img { position: absolute; inset: 0; }

.sp-event-grid { display: grid; gap: var(--sp-space-24); grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); }

/* ---------- Facts list (widgets + handoff docs) */
.sp-facts { margin: 0; border-top: 1px solid var(--sp-color-divider); }
.sp-facts__row { display: grid; grid-template-columns: minmax(110px, 30%) 1fr; gap: var(--sp-space-16); padding: var(--sp-space-12) 0; border-bottom: 1px solid var(--sp-color-divider); }
.sp-facts dt { font-size: var(--sp-type-caption); color: var(--sp-color-muted); }
.sp-facts dd { margin: 0; font-weight: 500; }
.sp-facts__todo { color: var(--sp-color-muted); }   /* missing fact: show it in grey words, never invent it */

/* ---------- Status notice: status block → what happened → next step → updated → action */
.sp-notice { display: grid; grid-template-columns: 184px 1fr auto; align-items: stretch; border-radius: var(--sp-radius); overflow: hidden; background: var(--sp-color-surface); }
.sp-notice__status { display: flex; flex-direction: column; justify-content: center; gap: 6px; padding: 0 var(--sp-space-20); background: var(--sp-color-accent); color: var(--sp-color-on-accent); }
.sp-notice__status-en { display: flex; align-items: center; gap: 6px; font-size: 11px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; }
.sp-notice__status-en::before { content: ""; width: 6px; height: 6px; border-radius: 3px; background: currentColor; }
.sp-notice__status-cn { font-size: 20px; font-weight: 700; line-height: 1.25; }
.sp-notice__body { display: grid; gap: 4px; padding: var(--sp-space-20) var(--sp-space-24); }
.sp-notice__msg { font-weight: 700; }
.sp-notice__next { font-size: var(--sp-type-caption); color: var(--sp-color-muted); }
.sp-notice__time { font-size: 12px; color: var(--sp-color-muted); }
.sp-notice__action { display: flex; align-items: center; padding-right: var(--sp-space-24); }
.sp-notice--attention .sp-notice__status { background: var(--sp-color-emphasis); color: var(--sp-color-on-emphasis); }
.sp-notice--critical { border: 1px solid var(--sp-color-emphasis-text); }
.sp-notice--critical .sp-notice__status { background: transparent; color: var(--sp-color-emphasis-text); border-right: 1px solid var(--sp-color-emphasis-text); }
@media (max-width: 640px) {
  .sp-notice { grid-template-columns: 1fr; }
  .sp-notice__status { padding: var(--sp-space-12) var(--sp-space-20); }
  .sp-notice__action { padding: 0 var(--sp-space-24) var(--sp-space-20); }
  .sp-event-card--row { flex-direction: column; }
  .sp-event-card--row .sp-event-card__media { width: 100%; aspect-ratio: 4 / 5; min-height: 0; }
}
```

Web fonts link:
```html
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&family=Noto+Sans+SC:wght@400;500;700;900&display=swap" rel="stylesheet">
```

## WeChat framework B modules (inline styles; framework A is the same except: M01 header image instead of F1 + poster, section chips `background:#73F64B;color:#111318`, key-point bar and ticket-card top line `#111318`, divider `#73F64B`)
```html
<section id="sp-article" style="font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Helvetica Neue','Microsoft YaHei',sans-serif;font-size:16px;line-height:1.8;color:#111318;letter-spacing:0.5px;">

<!-- F1 主办条 Host bar · 固定区 · 图片。海报偏暗用 hostbar-dark-1080.png，偏亮用 hostbar-light-1080.png -->
<section style="margin:0 -16px;"><img src="hostbar-dark-1080.png" alt="SinoPOP 主办 Presented by SinoPOP" style="display:block;width:100%;height:auto;"></section>

<!-- 艺人海报 Poster：艺人方原图，整张放，不裁切、不压字 -->
<section style="margin:0 -16px 28px;"><img src="poster.png" alt="艺人海报" style="display:block;width:100%;height:auto;"></section>

<!-- M02 导语 Lead -->
<p style="margin:0 0 24px;font-size:17px;line-height:1.8;color:#111318;font-weight:500;">[导语：艺人是谁、这次巡演带来什么。语气跟随艺人方文案。]</p>

<!-- M04 章节标题（借色编号 + 墨色标题） -->
<section style="margin:40px 0 16px;">
  <span style="display:inline-block;padding:2px 10px;background:#1863C3;color:#FFFFFF;border-radius:8px;font-size:15px;font-weight:800;">01</span>
  <span style="margin-left:10px;font-size:21px;font-weight:700;line-height:1.4;color:#111318;vertical-align:middle;">演出信息</span>
</section>

<!-- M05 正文 -->
<p style="margin:0 0 16px;">[巡演介绍 / 曲目亮点 / 艺人方提供的文案，原文照录并注明出处。]</p>

<!-- M10 分隔（借色） -->
<section style="margin:32px 0 24px;"><span style="display:inline-block;width:48px;height:3px;background:#1863C3;"></span></section>

<!-- M06 重点（纸白底 + 借色左线） -->
<section style="margin:24px 0;padding:14px 16px;background:#F7F8F4;border-left:4px solid #1863C3;border-radius:8px;">
  <p style="margin:0;font-size:13px;font-weight:700;color:#5A616C;letter-spacing:2px;">重点</p>
  <p style="margin:4px 0 0;font-size:16px;font-weight:500;color:#111318;">[入场须知 / 年龄限制 / 禁止携带物品。]</p>
</section>

<!-- M07 图片（可选：阵容图、往期现场。海报类原比例不裁切） -->

<!-- M09 提醒 Notice（单色，不借色：状态信息永远是 SinoPOP 的） -->
<section style="margin:24px 0;padding:14px 16px;border:1.5px solid #111318;border-radius:8px;">
  <p style="margin:0;"><span style="display:inline-block;padding:1px 8px;background:#111318;color:#FFFFFF;border-radius:8px;font-size:12px;font-weight:700;letter-spacing:1px;">注意 NOTICE</span></p>
  <p style="margin:8px 0 0;font-size:15px;color:#111318;">[发生了什么]。[观众需要做什么 / 已购票怎么办]。</p>
  <p style="margin:4px 0 0;font-size:13px;color:#5A616C;">更新于 [MM.DD HH:MM]</p>
</section>

<!-- 购票章节 -->
<section style="margin:40px 0 16px;">
  <span style="display:inline-block;padding:2px 10px;background:#1863C3;color:#FFFFFF;border-radius:8px;font-size:15px;font-weight:800;">02</span>
  <span style="margin-left:10px;font-size:21px;font-weight:700;line-height:1.4;color:#111318;vertical-align:middle;">购票</span>
</section>

<!-- F2 购票卡 · 固定区 · 必须是文字。只有顶线用借色 -->
<section style="margin:0 0 32px;padding:18px 20px 20px;background:#F7F8F4;border-top:4px solid #1863C3;border-radius:8px;">
  <p style="margin:0;font-size:12px;font-weight:700;color:#5A616C;letter-spacing:1px;">购票信息 TICKETS</p>
  <p style="margin:6px 0 0;font-size:20px;font-weight:700;color:#111318;">10.24 SAT · 19:30</p>
  <p style="margin:2px 0 12px;font-size:17px;font-weight:700;line-height:1.4;color:#111318;">[艺人名 巡演标题] · [城市站]</p>
  <section style="border-top:1px solid #D8DBD3;padding:10px 0;font-size:15px;"><span style="display:inline-block;width:7.2em;font-size:14px;color:#5A616C;">场地 Venue</span><span style="font-weight:500;">[场地名称 · 地址]</span></section>
  <section style="border-top:1px solid #D8DBD3;padding:10px 0;font-size:15px;"><span style="display:inline-block;width:7.2em;font-size:14px;color:#5A616C;">票价 Price</span><span style="font-weight:500;">[USD 00 起]</span></section>
  <section style="border-top:1px solid #D8DBD3;border-bottom:1px solid #D8DBD3;padding:10px 0;font-size:15px;"><span style="display:inline-block;width:7.2em;font-size:14px;color:#5A616C;">开票 On sale</span><span style="font-weight:500;">[MM.DD DAY 12:00 PT]</span></section>
  <p style="margin:16px 0 0;"><span style="display:inline-block;padding:8px 14px;background:#111318;color:#FFFFFF;border-radius:8px;font-size:14px;font-weight:700;">点击「阅读原文」购票</span><span style="float:right;margin-top:8px;font-size:12px;color:#5A616C;">主办 SinoPOP</span></p>
</section>

<!-- F3 客服区 · 固定区 -->
<section style="margin:0 0 20px;overflow:hidden;">
  <img src="qr.png" alt="客服二维码" style="float:right;width:112px;height:112px;margin-left:16px;border:1px solid #D8DBD3;border-radius:8px;">
  <p style="margin:0 0 6px;font-size:18px;font-weight:700;">购票与咨询</p>
  <p style="margin:0;font-size:15px;">购票：点击左下角「阅读原文」</p>
  <p style="margin:0 0 8px;font-size:12px;color:#5A616C;">Tickets: tap “Read more” below</p>
  <p style="margin:0;font-size:15px;">咨询与售后：扫码添加 SinoPOP 客服</p>
  <p style="margin:0;font-size:12px;color:#5A616C;">Questions &amp; refunds: scan to add our service account</p>
</section>
<section style="margin:0 -16px;"><img src="brandbar-1080.png" alt="SinoPOP 主办 · 现场见" style="display:block;width:100%;height:auto;"></section>

</section>
```