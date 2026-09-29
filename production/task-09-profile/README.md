# 主办方介绍竖版模板

依据 V25 排版，提供 A4、Letter 与手机竖版三种比例。各套均为 6 页：封面、曲目目录、01 我们是谁、02 我们做什么、03 做过的现场、04 合作方式与联系。目录最后一条合并合作与联系，与本轮规定的六页顺序一致。

| 路径 | 用途与尺寸 |
| --- | --- |
| `a4/profile-a4-rgb.pdf` | 6 页 RGB 打样；成品 210 × 297 mm |
| `a4/profile-a4-print.pdf` | 同版 CMYK + SP-GREEN 印刷文件 |
| `letter/profile-letter-rgb.pdf` | 6 页 RGB 打样；成品 8.5 × 11 in（215.9 × 279.4 mm） |
| `letter/profile-letter-print.pdf` | 同版 CMYK + SP-GREEN 印刷文件 |
| `a4/*-p01.svg` 至 `*-p06.svg` | 可编辑矢量页面，内嵌字体子集、原始标志与封面图 |
| `letter/*-p01.svg` 至 `*-p06.svg` | 可编辑的 Letter 页面 |
| `a4/*-preview.png`、`letter/*-preview.png` | 长边至少 2400 px 的逐页预览 |
| `mobile/*-p01.svg` 至 `*-p06.svg` | 1080 × 1920 px 可编辑手机模板 |
| `mobile/*-preview.png` | 六张精确 1080 × 1920 px 手机图片 |
| `mobile/profile-mobile-rgb.pdf`、`*-print.pdf` | 手机版六页审阅合集；PDF 内部等比画布为 381 × 677.33 mm，手机发布请使用 PNG |
| `*-layout.json`、`profile-metadata.json` | 文本、字号、基线与尺寸记录 |
| `build-profile.py` | 通过共享 `../production.py` 重新导出三套模板 |

印刷 PDF 四边出血均为 3 mm，带裁切线、TrimBox 与 BleedBox。此模板没有模切、打孔或折线，因此不附工艺 PDF。页内文字为可编辑文本，不是文字图片；使用 Archivo Regular/Bold/ExtraBold 与 Noto Sans SC Regular/Bold/Heavy。纸张版本最小字号 7.5 pt。新增字符时应安装总包 `assets/fonts` 里的字体，修改脚本后重新导出，以更新嵌入子集。

平面色值限于本轮八色；大面积深色背景改为层级面 `#181A1F`。亮绿均用于深色背景文字或黑字色块，没有亮绿色浅底文字。原标志 SVG 未改色、未描边，按原比例放置；标志自身原有的黑/白色与照片自然像素不作为平面色板违例。

已知正文只使用「从华语青年音乐与文化出发，把现场带给海外的年轻观众。」；三项服务标题使用本轮指定文字，其余介绍、合作、联系人、活动、日期、场地、摄影等均为方括号占位。填入真实活动信息后，需重新检查换行与字体子集。

封面使用上一轮已验收的 `profile-cover-square.png` 与 `profile-cover-phone.png`。两张都是 AI 氛围图，页面上有明确标注，不能作为已举办活动的证据。第五页只放真实活动照片的空框，明确要求填写摄影；没有把 AI 图放进实绩页。手机封面保持原图 9:16 比例，并叠加可编辑的播放器信息与真标志。

印厂注意：亮绿需要荧光专色打样；矢量亮绿已分至命名为 `SP-GREEN` 的专色版，不指定厂商色号。照片在印刷版中转为 CMYK，其自然绿色仍在照片 CMYK 图像内，不等同于平面亮绿专色。CMYK 预览不等于实物荧光色；按承印材料做实物比对。黑色或深色卡材上的白字需要白墨版；本套默认白纸承印、深色背景印刷，改用深色基材时请由印厂分出白墨底版。

重建：在总包根目录运行 `python task-09-profile/build-profile.py`，依赖总包的共享生产引擎与字体。脚本优先读取上轮已验收照片；便携交付缺少独立照片文件时，会从现有封面 SVG 的内嵌原图中恢复输入，不重新生成照片。
