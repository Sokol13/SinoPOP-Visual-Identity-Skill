# sinoPOP Design System — rules for AI agents (v2.1)

sinoPOP is a music & live-culture **promoter** rooted in Chinese youth music, bringing live shows to young audiences abroad. You are building one of four things: **web widgets**, **WeChat Official Account articles (公众号)**, **handoff documents (交接文件)**, or **on-site / print production files** (cards, wristbands, passes, signage, roll-ups, promoter profile). Read this file first, then use the files it points to. Do not invent a new style.

## Files
| Need | Use |
|---|---|
| Colors, type, spacing, radius | `tokens/tokens.json` (source) → `tokens/tokens.css` (run `python3 tokens/build.py` after editing) |
| Web widgets (Wix embed or V2 site) | `web/sinopop-widgets.css` + `tokens/tokens.css`; examples in `web/widgets-demo.html`; paste-ready Wix embeds in `web/embed/` |
| WeChat article | Framework A (self-run, no specific artist): `wechat/article-template.html` · Framework B (artist-led, poster first): `wechat/article-artist.html` — inline styles only |
| Handoff doc | Figma page `30 · 组件 2.0` → `Template/A4 …` and `Template/1080 …`; Google Docs: `handoff/google-docs-guide.md` |
| Print / on-site items | Visual rules: Figma page `82 · VI规范 2.0`, frames V24–V29 (PDF: `sinoPOP-VI规范-2.1-定稿.pdf`). Production files, scripts and sample CSVs: the `sinopop-music-objects/` package (`task-04-card-final` … `task-09-profile`) — rebuild with its scripts, never redraw by hand |
| Logo | `assets/sinopop-logo-white.svg`, `assets/sinopop-logo-black.svg` (vector trace of the approved brush PNG) |
| Figma | File `oQLs4rdfXbgzhLE0XDpTri`. Variables: `sinoPOP / Primitives`, `sinoPOP / Color` (modes Dark, Light), `sinoPOP / Dimensions`. Each variable's WEB code syntax = the CSS variable. Each component description lists USE / DON'T / PROPS / CODE / TOKENS. |

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
8. **Never invent facts** (dates, venues, prices, artists, contacts, fees). If missing, write `待确认 To be confirmed` (web: `.sp-facts__todo`; Figma: `Web/FactRow State=TBC`).
9. Artist posters are artwork: show whole (`object-fit: contain`), never crop, never type over them. Show photos may be cropped (`cover`) if the performer and action survive.
10. Logo: black or white version only, transparent background. Never redraw, retype, recolor, outline, add effects, box, stretch or rotate. White on dark, black on light.
11. Status must be written in words (bilingual). Color only supports it. Every status notice says what happens next.
12. In mixed-bilingual pieces: Chinese first, English second, same order throughout.

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
Figma text styles: `sinoPOP 2.1 / zh / …` and `sinoPOP 2.1 / en / …`. Demo: `web/lang-switch-demo.html`.

## Themes
- Web widgets: Dark (default). Add `data-sp-theme="light"` on a wrapper for light sections.
- WeChat article body and handoff docs: Light. Brand dark lives in the header image (framework A), the host bar (framework B) and the brand bar in the service footer.
- In Figma, set the outer frame's `sinoPOP / Color` mode to Light; bound components switch automatically.

## Web widgets
- Wrap everything in `<div class="sp-root">`. Classes: `.sp-btn[--secondary|--ghost][--s]`, `.sp-tag--soon|--waitlist|--on-sale|--tonight|--selling-fast|--changed|--postponed|--sold-out|--ended|--cancelled`, `.sp-event-card[--row]`, `.sp-event-grid`, `.sp-facts` / `.sp-facts__row` / `.sp-facts__todo`, `.sp-notice[--attention|--critical]` (status block + message + next step + updated time), `.sp-section-head`.
- Wix: Add → Embed Code → Embed HTML → paste a file from `web/embed/` and edit only the markup.
- V2 site: import `tokens.css` + `sinopop-widgets.css`; keep the class names (port to components 1:1 if using React).
- Buttons ≥ 48px tall (`--sp-control-m`); one primary button per area; grid collapses to one column on phones.

## WeChat (公众号)
- Inline styles only. No `<style>`, no scripts, no web fonts, no external CSS. Deliver HTML; the person opens it in a browser, copies all, pastes into the WeChat editor. Check at 375 px and in dark mode.
- **Pick a framework first.** No specific artist (party, theme night) → **A** `article-template.html`: full sinoPOP look (dark header image with white logo, green section numbers, ink key-point bar). Artist show with a poster → **B** `article-artist.html`: poster-led middle, sinoPOP at top and bottom.
- **Three fixed zones — identical in A and B, never restyled:**
  - F1 Host bar (B only, first thing in the article): `hostbar-dark-1080.png` / `hostbar-light-1080.png` (match the poster's lightness). Figma `WX/HostBar`.
  - F2 Ticket card (in the 购票 section): must be text — date, title, venue, price, on-sale time, ink CTA 「点击「阅读原文」购票」, 主办 sinoPOP. Figma `WX/TicketCard`.
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
- Every page: `Doc/Footer` — left `sinoPOP · 内部资料 Internal`, center file name, right page `1 / 2` (Archivo).
- Body: `Doc/SectionTitle` → `Web/FactRow` (label 14 #5A616C, value 16 Medium #111318, TBC in muted grey `--sp-color-muted`) / `Doc/ScheduleRow` / `Doc/QuoteRow` (numbers right-aligned, USD) / `Doc/CheckItem` / `Doc/SignBlock`.
- WeChat long image: lay out at 450 wide, export ×2.4 = 1080 wide PNG.
- File name: `sinoPOP_{类型}_{艺人}_{城市}_v01_YYYYMMDD.pdf`. Bump the version on every change and update the header.

## On-site credentials (wristbands, passes, lanyards)
- Wristbands are for the audience only and follow the ticket tier: white/paper = GA (early bird is the same tier), green = VIP, ink black = SVIP / table (卡座, top tier). Tier is always written in words; every band carries a serial number; logo on the band (black on white/green, white on black).
- Staff, artists and guests never wear wristbands; they use passes. No "ALL ACCESS" wording anywhere.
- Passes (90 × 130 mm) show role + numbered access zones (1 floor · 2 backstage · 3 stage · 4 green room). Roles: STAFF (green band), ARTIST (ink band, thick green outline), ARTIST TEAM (ink band, thin green outline), GUEST (paper band), PRESS (grey band), PRODUCTION (ink band, grey outline).
- Lanyards show which side you belong to: green = sinoPOP team, black with green print = artist side (artist + artist team), white = guests, grey = press and production.
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
- Promoter profile: only the confirmed line 「从华语青年音乐与文化出发，把现场带给海外的年轻观众。」 is real copy; everything else stays `[占位]` until the person supplies it. Past-show pages need real event photos with photographer credit — AI images are mood only and never presented as sinoPOP events.
- QR boxes are placeholders; replace with a real code and test-scan before print.

## Voice
Bold but clear. Lead with date, venue, price, next step. No unverifiable superlatives (史上最强 / the biggest ever). No "stay tuned" without a date or next step.

## Before you finish, check
Contrast ≥ 4.5:1 for text · no TBC left in public versions · viewed at 375px wide · cover safe area holds title and date · correct logo version · version/date updated · image source & rights noted.
