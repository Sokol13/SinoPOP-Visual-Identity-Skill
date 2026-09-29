# 名片产品摄影生成记录

6 张底图全部使用内置 image_gen 独立生成，保留无文字、无标志的表面，供后续真 SVG 标志和真实字体排版合成。所有底图为 AI 产品概念图，不是实拍打样；原生 1448 × 1086 px，交付成图需放大到长边至少 2400 px。模型中自然光照及真实材质会产生连续色阶，精确品牌色仅适用于确定性图形层。

## 1. 01-ticket

文件：`task-01-cards/01-ticket/mockup-raw.png`

原始文件：`C:\Users\sokol\.codex\generated_images\01a0e65b-d06b-7360-985b-8e9fcc39acd5\exec-0d389253-a3ef-4fee-83e3-4522ae38213c.png`

合成参考：White original logo on black left field around x 355-630, y 405-650; preserve aspect ratio and no effect.

主表面四角（原图像素，左上/右上/右下/左下）：`[[238,294],[973,294],[980,758],[237,757]]`

英文生图提示词：

```text
Use case: product-mockup. Photorealistic premium editorial product photograph for a Chinese youth music promoter. One US-standard horizontal business card, 3.5 by 2 inches, main left two thirds matte ink black (#111318), right one third vivid flat green (#73F64B). The right ticket stub is half torn along a vertical perforation with two semicircular notches at the top and bottom of the perforation. Still attached at the bottom, stub bent only slightly upward. The card lies on dark charcoal concrete, severe white hard side lighting, tactile uncoated card stock and credible fine paper fibers, subtle film grain. Camera nearly perpendicular looking down, single hero card centered, card itself horizontally aligned, enough margins around it. NO writing at all, no letters, no numbers, no logos, no symbols, no watermark; all black and green print surfaces must remain completely blank for deterministic artwork compositing afterward. Do not create a brand mark. Real photography, not 3D rendering, no glow, no metallic effect, no fake bevel. All visible hues restricted to neutral ink black, charcoal, paper white, grays and vivid green; no red, amber, pink. Landscape 4:3 image, at least 2400 pixels on the long edge, high detail.
```

## 2. 02-setlist

文件：`task-01-cards/02-setlist/mockup-raw.png`

原始文件：`C:\Users\sokol\.codex\generated_images\01a0e65b-d06b-7360-985b-8e9fcc39acd5\exec-b69c79b6-f95e-47fd-9d78-30526e8e1f48.png`

合成参考：Black original logo small on white card lower right around x 940-1050, y 595-680; title and contacts between y 370-645.

主表面四角（原图像素，左上/右上/右下/左下）：`[[368,268],[1077,268],[1094,712],[348,712]]`

英文生图提示词：

```text
Use case: product-mockup. Premium photorealistic editorial close-up of one US-standard 3.5 by 2 inch horizontal paper-white (#F7F8F4) business card taped onto the front of a real black stage wedge monitor speaker. A narrow vivid green (#73F64B) strip of torn-edge gaffer tape across the card's top edge, matte paper with subtle grain, entirely blank white card surface for later precise typography compositing. One thin horizontal ink-black line printed beneath the green tape, otherwise no writing whatsoever. The stage monitor's black cloth grille and rugged charcoal frame recognizable around the card, dark rehearsal stage background, white practical side light, documentary texture, no colored stage lights. Camera nearly normal to the card face so the full rectangular card is a clean flat plane; card occupies about 60 percent image width and sits centered, horizontal edges, minimal perspective. No logos anywhere on the card or speaker, no letters, no numbers, no readable labels, no watermark. Restrict hues to neutral ink black, charcoal, grays, paper white and vivid green; no red, amber or pink. Real physical photograph not 3D. Landscape 4:3 composition at least 2400 pixels long edge.
```

## 3. 03-vinyl

文件：`task-01-cards/03-vinyl/mockup-raw.png`

原始文件：`C:\Users\sokol\.codex\generated_images\01a0e65b-d06b-7360-985b-8e9fcc39acd5\exec-5b0ccdb4-8cb0-46db-8a8b-cd49fa1b89e8.png`

合成参考：White original logo on sleeve left blank field x 630-800, y 350-560; inner card contact area x 175-510, y 260-730.

主表面四角（原图像素，左上/右上/右下/左下）：`[[550,219],[1317,219],[1317,793],[545,793]]`

英文生图提示词：

```text
Use case: product-mockup. Premium tactile editorial product photograph: a tiny 3.5 by 2 inch horizontal matte ink-black paper record sleeve business card resting on a weathered record-store wooden crate. The black outer sleeve has a clean circular die-cut window in the right half, revealing a vivid green (#73F64B) printed vinyl disc on a matching inner card, realistic concentric black hairline record grooves, green center label left completely blank. Inner card partially pulled from the sleeve toward the left so a blank paper-white rectangular information area is visible. All surfaces intentionally blank for later true typography and original logo compositing, no text, no letters, no numbers, no icons, no logos anywhere in scene. Main card front nearly parallel to camera, horizontal card long edges; minimal perspective. Composition close-up central product with wooden slats and blurred neutral record sleeves in background. Warm-feeling soft white practical light but neutral/desaturated wood, no amber/orange color cast; deep ink-black shadows, occasional green only. Fine film grain, authentic paper fibers, tiny physical die-cut edges. Real camera photo not CGI, no glossy metallic effects, no glow, no fantasy 3D. Colors restricted to ink black #111318, charcoal #1B1E24, paper white #F7F8F4, green #73F64B and neutral grays. Landscape 4:3 image, at least 2400 pixels long edge.
```

## 4. 04-backstage

文件：`task-01-cards/04-backstage/mockup-raw.png`

原始文件：`C:\Users\sokol\.codex\generated_images\01a0e65b-d06b-7360-985b-8e9fcc39acd5\exec-4c5dd9ef-2099-45cc-aa2d-5eeef0032b09.png`

合成参考：White original logo on center card lower area x 730-840, y 750-850; centered name above green band and ALL ACCESS on band y 534-668. Side cards optionally use similar true artwork.

主表面四角（原图像素，左上/右上/右下/左下）：`[[549,314],[874,314],[878,882],[547,882]]`

英文生图提示词：

```text
Use case: product-mockup. Premium documentary product photograph of exactly three vertical backstage-pass business cards hanging from vivid green (#73F64B) fabric lanyards draped over a black microphone stand, small music venue backstage. Each card has 2 by 3.5 inch proportions, matte ink-black (#111318) thick stock, modest 2 mm rounded corners, one genuine horizontal lanyard slot near the top. A simple flat green horizontal band across the middle of each card, otherwise completely blank black face, no print at all. Middle hero card completely visible, facing the camera directly, large in frame. Other two cards offset left and right behind, also nearly facing camera, not covering middle card. Upper third and lower third of each face blank for later precise typography/logo overlays; green band blank for later ALL ACCESS lettering. Camera level with the cards, shallow but sufficient depth of field to read paper texture, dark charcoal stage background, realistic white rehearsal light and very subdued green practical light. No people, no letters, no numbers, no invented logos, no watermarks, no shiny holograms. Hues restricted to ink black, charcoal, white, neutral grays, vivid green, avoid pink red amber. Real physical photograph, no CGI, no glow, no fake 3D. Landscape 4:3 at least 2400 pixels on the long edge.
```

## 5. 05-jcard

文件：`task-01-cards/05-jcard/mockup-raw.png`

原始文件：`C:\Users\sokol\.codex\generated_images\01a0e65b-d06b-7360-985b-8e9fcc39acd5\exec-bfc0d605-6bad-458f-95d2-9ff66bcbc181.png`

合成参考：White original logo in black case cover x 365-600, y 630-805; use strict proportional logo and avoid geometric deformation. Upper right open white panel x 520-890,y 120-570 may receive black contacts.

主表面四角（原图像素，左上/右上/右下/左下）：`[[202,510],[817,626],[780,981],[93,848]]`

英文生图提示词：

```text
Use case: product-mockup. Ultra-realistic premium editorial product photograph of two clear audio cassette cases with folded matte paper J-card business-card inserts, one case closed and the other open, sitting on dark charcoal concrete. J-card is a compact real three-panel fold: a large horizontal cover panel, a narrow spine, and a shorter back flap. Ink-black (#111318) cover with one single thin vivid-green (#73F64B) horizontal rule near lower edge, completely blank otherwise; white interior panel, blank spine, no letters, numbers, graphics or logos whatsoever. Main closed case in the lower left of the image with its black cover facing straight toward the camera, minimal perspective, clear edges and empty cover space for later authentic artwork overlay. The open case in the upper right reveals blank paper-white inside of the folded J-card; believable transparent plastic hinges and rounded corners. No cassette label printing and no fake brands, no text anywhere. Macro studio photography with hard white sidelight, delicate reflections on clear plastic, matte paper texture visible, shallow depth of field but main cover sharp. Actual physical photograph not 3D rendering, no metallic graphic effect, no glow, no lens flare. Hues limited to ink black, charcoal, paper white, neutral gray and vivid green, never amber red pink. Landscape 4:3 at least 2400 pixels on long edge.
```

## 6. 06-material

文件：`task-01-cards/06-material/mockup-raw.png`

原始文件：`C:\Users\sokol\.codex\generated_images\01a0e65b-d06b-7360-985b-8e9fcc39acd5\exec-3d649a8e-ee73-411c-8dcf-1458aa40e385.png`

合成参考：White original logo modest in broad black top surface x 1040-1210,y 350-460; Chinese name on top surface x 440-850,y 370-525. Preserve true logo proportions, no simulated logo deboss.

主表面四角（原图像素，左上/右上/右下/左下）：`[[109,318],[1124,152],[1384,480],[281,692]]`

英文生图提示词：

```text
Use case: product-mockup. Premium extreme-close-up editorial macro product photograph of exactly ten exceptionally thick 600 gsm black cotton-paper business cards stacked neatly, with vivid green (#73F64B) hand-painted edges revealed clearly along the long and short faces. US-standard 3.5 by 2 inch cards, matte ink-black (#111318) cotton faces with visible natural paper fibers, very subtle rounded corners. The top card is completely blank, no typography, no debossed fictional mark, all blank to later composite exact Chinese name and original logo. Stack placed on neutral dark concrete, close low camera angle but enough top surface visible and evenly sharp for typography placement. Top long edges nearly horizontal across image with mild perspective only. Green edges crisp but authentic slightly imperfect brush pigment, total stack about 8 mm thick; resolve ten separate dark-paper strata. One hard white studio side light rakes across paper fibers and painted edges, dramatic shadows, fine photographic grain. Real photograph, no CGI, no gloss, no metallic foil, no glow, no fake bevel. No letters, logos, numbers, symbols, watermark, red, amber or pink anywhere. Color palette black, charcoal, neutral grays, paper white highlights and vivid green only. Landscape 4:3 image at least 2400 pixels on the long edge, tactile luxury print craftsmanship.
```


## 最终合成验收

6 张 mockup.png 已于本任务内完成：2400 × 1800 px，均已解码和目视检查。字体与原始 SVG 标志通过透明油墨图层合成；纸张、木箱、绳带、透明盒和刷边保留摄影质感。票根、黑胶两张近正面主标志单独等比放置，避免生成底图的物件比例偏差拉伸标志。后台证等倾斜纸面呈现物理透视，源标志文件未经改动。原生底图 1448 × 1086 px，最终使用 Lanczos 放大；不宣称原生 2400 px 细节或真实印刷打样。所有生图均为 AI 概念效果，不能充当 sinoPOP 真实活动或实物生产记录。

