# 莫耳之戰：饒舌對決教學影片（第 3 週・莫耳與化學式）

配合課程投影片 [新W03_莫耳與化學式](https://tai-shengyeh.github.io/general-chemistry/%E6%96%B0W03_%E8%8E%AB%E8%80%B3%E8%88%87%E5%8C%96%E5%AD%B8%E5%BC%8F.html#1)，
用 [shanshiba-workflow-colab](https://github.com/mathruffian-dot/shanshiba-workflow-colab) 的饒舌對決範本（`pipeline/template_battle/`）製作的整場設定。
這個資料夾是**成片的輸入**：`battle.json`（人物、兩首歌詞、DJ 口白、擂台與閃回場景、字卡、51 鏡鏡表）＋ `songtext/`（已產生的 YuE2 與 Suno 歌詞、風格文字）。
**生歌用 YuE2**（在 Colab 上跑，不需要 Suno 帳號）；`battle.json` 的段落與鏡頭時間已照 YuE2 調好，改用 Suno 也一樣能跑。
真正的生歌、首幀、H3 影片要在你的 Colab（或本機顯卡）上跑，步驟見最下面。

## 對決設計

| 項目 | 內容 |
|:--|:--|
| 片名 | 莫耳之戰 |
| A（先出場，鈷藍方） | **道耳頓** John Dalton：原子論、第一張原子量表；把水寫成 **HO** |
| B（後出場，鈉黃方） | **亞佛加厥** Amedeo Avogadro：分子假說、雙原子氣體、水是 **H2O**；莫耳的「個數」 |
| DJ（電弧銀白） | **戴維** Humphry Davy：1807 電解出鈉、1810 確認氯是元素（食鹽 NaCl 的兩種元素都跟他有關）；1826 以皇家學會會長頒獎章給道耳頓 |
| 爭點 | 只知道**質量比**，能不能決定**化學式**？（HO vs H2O） |
| 結局 | 史實定論：道耳頓給「一顆多重」（原子量），亞佛加厥給「一莫耳幾顆」（個數）→ 合起來＝**莫耳質量 g/mol** |
| 投票 | 挺道耳頓打「原子」，挺亞佛加厥打「莫耳」 |
| 配色 | 左鈷藍（曼徹斯特雨天、鈷玻璃）｜右鈉黃（鈉的焰色 589 nm，呼應「鈉 1800 mg」錨點）；DJ 銀白（電弧） |

**對到本週學習目標**

| 學習目標 | 片中哪裡 |
|:--|:--|
| 莫耳＝數個數的單位、NA | A 12–13、B 18、B 23 殺句；字卡 `perrin`、`water` |
| g ↔ mol ↔ 粒子數 三向換算 | **B 的唱段（第 8–11 句）整段就是三向換算**；字卡 `triway`、黑板插入鏡 F10 |
| 由質量比反推化學式、實驗式 vs 分子式 | A 4–5、A 8；B 12–15；字卡 `ho`、`o7`、`empirical` |
| 元素 vs 化合物：鈉 ↔ 鹽 | B 19「泡麵鈉 1800 mg × 2.54 ≈ 4.6 g 鹽」；字卡 `sodium`、廚房秤插入鏡 F13 |

## DJ 口白

| 位置 | 口白 |
|:--|:--|
| open | 化學史大擂台！莫耳之戰！英國的道耳頓，對上，義大利的亞佛加厥！水的化學式，到底誰寫對？開打！ |
| switch | 被說是律師來亂？亞佛加厥，反擊的時間到了！上台！ |
| verdict | 道耳頓給了原子量，亞佛加厥給了個數。兩個加起來，就是莫耳質量！ |
| end | 誰贏了？下一場是誰？你決定！ |

## A：道耳頓（16 句，144 BPM，深沉沙啞男中音，工業 boom-bap＋大提琴）

| # | 段落 | 歌詞（字幕） | 韻腳 |
|:--|:--|:--|:--|
| 0 | Verse | 1808 我出新書　原子理論我寫第一部 | 一部 |
| 1 | Verse | 每種元素一種原子　這是化學的基礎 | 基礎 |
| 2 | Verse | 原子不能切、不能毀　也不能憑空變出 | 變出 |
| 3 | Verse | 律師跨界來亂　你先回去學好算數 | 算數 |
| 4 | Verse | 第一張原子量表我排　氫算 1　其他都跟它比重量 | 重量 |
| 5 | Verse | 一氧化碳、二氧化碳　氧就差 2 倍　整數比是我的主張 | 主張 |
| 6 | Verse | 57 年天天記天氣　一筆一筆數據我最穩當 | 穩當 |
| 7 | Verse | 你的假說一張紙　沒做實驗只會空想 | 空想 |
| 8 | Verse | 水就是一個氫配一個氧　最簡單的比例最可靠 | 可靠 |
| 9 | Verse | 你偏要把氧劈成兩半　原子能切？誰教你這套 | 這套 |
| 10 | Verse | 法國人的體積數據我說不準　你還拿來當寶 | 當寶 |
| 11 | Verse | 伯爵先生名字一長串　論文放了 50 年沒人看到 | 看到 |
| 12 | Final Build | 那個 6.02 × 10²³　不是你量　也不是你算 | 你算 |
| 13 | Final Build | 1909 法國人量出來　你的名字才跟著流傳 | 流傳 |
| 14 | Final Build | 原子理論是我打的地基　化學大樓我一手蓋完 | 蓋完 |
| 15 | Final Build | 你的莫耳只是我頂樓的違章加蓋　一拆就散 | 就散 |

## B：亞佛加厥（24 句，含 4 句唱段，144 BPM，明亮尖銳男高音，義大利巴洛克 trap＋曼陀林）

| # | 段落 | 歌詞（字幕） | 韻腳 |
|:--|:--|:--|:--|
| 0 | Verse | 1811 我只寫一篇　就把你整本書修補 | 修補 |
| 1 | Verse | 同溫、同壓、同體積　氣體分子個數都相符 | 相符 |
| 2 | Verse | 律師出身我只看證據　你的 HO 證據不足 | 不足 |
| 3 | Verse | 57 年天天記雨　也洗不掉你的糊塗 | 糊塗 |
| 4 | Verse | 原子不能切我同意　但氧氣是兩顆手牽手 | 牽手 |
| 5 | Verse | 我劈的是分子不是原子　你分不清還敢開口 | 開口 |
| 6 | Verse | 2 份氫、1 份氧　變成 2 份水蒸氣　你算不通就溜走 | 溜走 |
| 7 | Verse | 法國人的數據你不肯看　還說我空想不動手 | 動手 |
| 8 | Melodic Hook | 公克 ÷ 莫耳質量　就變成莫耳 | （唱段） |
| 9 | Melodic Hook | 莫耳 × 亞佛加厥數　就變成個數 | （唱段） |
| 10 | Melodic Hook | 質量和個數　不能直接換 | （唱段） |
| 11 | Melodic Hook | 莫耳永遠是中間那一站 | （唱段） |
| 12 | Verse | 你的原子量表氧算 7　錯了一倍還不止 | 不止 |
| 13 | Verse | 水是 H2O　翻開課本每一頁都印著我的公式 | 公式 |
| 14 | Verse | 整數比我不否認　但比例不等於個數　這是常識 | 常識 |
| 15 | Verse | 甲醛、醋酸、葡萄糖　最簡比都是 CH2O　你分得出幾種東西 | 東西 |
| 16 | Pre-Chorus | 放了 50 年沒人看？1860 卡爾斯魯厄全場幫我翻案 | 翻案 |
| 17 | Pre-Chorus | 名字長是因為要寫進每一題莫耳計算 | 計算 |
| 18 | Final Build | 1 莫耳的水才 18 克　一大匙就裝得滿 | 得滿 |
| 19 | Final Build | 泡麵鈉 1800 mg 乘上 2.54　4.6 克鹽有多鹹 | 多鹹 |
| 20 | Final Build | 沒有莫耳　你的原子量只能掛在牆上好看 | 好看 |
| 21 | Final Build | 你說我違建？整棟化學靠我這根大樑才不會斷 | 會斷 |
| 22 | Final Build | 地基你打沒錯　可是一樓的水你就寫錯一半 | 一半 |
| 23 | Final Build | 你連兩顆氫都數錯　我一口氣數到 6.02 × 10²³ | 10²³ |

## 兩邊對照表（A 丟的點 → B 怎麼接）

| A | A 丟的點 | B | B 怎麼接 |
|:--|:--|:--|:--|
| 0 | 1808 出書，原子論第一部 | 0 | 1811 只寫一篇就修補你整本書 |
| 1–2 | 原子不能切、不能毀 | 4–5 | 同意原子不能切；氧氣是兩顆手牽手，劈開的是分子 |
| 3 | 律師跨界來亂 | 2 | 律師只看證據，你的 HO 證據不足 |
| 4 | 原子量表，氫＝1 | 12 | 你的表氧算 7，錯了一倍還不止 |
| 5 | 倍比定律、整數比 | 14–15 | 比例≠個數；CH2O 三種化合物分不出來（實驗式 vs 分子式） |
| 6 | 57 年天氣數據最穩 | 3 | 記 57 年雨也洗不掉糊塗 |
| 7 | 你沒做實驗只會空想 | 7 | 給呂薩克的數據你自己不肯看 |
| 8 | 水＝一個氫配一個氧，最簡單 | 6、13 | 2 體積氫＋1 體積氧→2 體積水氣，HO 算不通；課本印的是 H2O |
| 9 | 把氧劈成兩半？ | 5 | 劈的是分子不是原子 |
| 10 | 法國人的體積數據不準 | 6–7 | 用那組體積數據反證 |
| 11 | 名字長、論文 50 年沒人看 | 16–17 | 1860 卡爾斯魯厄翻案；名字長是要寫進每一題莫耳計算 |
| 12–13 | 6.02 × 10²³ 不是你算的，1909 才掛你名字 | 18、23 | 1 莫耳水只有一大匙；殺句：你連兩顆氫都數錯，我一口氣數到 6.02 × 10²³ |
| 14 | 原子論是我打的地基 | 22 | 地基沒錯，可是一樓的水你就寫錯一半（HO 少一個 H） |
| 15（殺句） | 你的莫耳是我頂樓的違章加蓋，一拆就散 | 21 | 整棟化學靠我這根大樑才不會斷 |

## 史實與出處（字卡用）

- 道耳頓原子論：J. Dalton, *A New System of Chemical Philosophy*, Part 1 (1808)。原子量表 1803 年宣讀、1805 年刊於 *Memoirs of the Literary and Philosophical Society of Manchester*；1808 表中以 H＝1、O＝7，並依「最簡單原則」把水寫成 HO。
- 倍比定律：Dalton 以一氧化碳／二氧化碳（及甲烷／乙烯）為例。
- 道耳頓天氣日誌：1787–1844 年，約 20 萬筆觀測。
- 給呂薩克氣體化合體積定律：J. L. Gay-Lussac, *Mémoires de la Société d'Arcueil* 2 (1809)，1808 年底發表；道耳頓不接受。
- 亞佛加厥假說：A. Avogadro, *Journal de Physique* 73, 58–76 (1811)；同溫同壓同體積氣體分子數相同、氫氧為雙原子分子。他原本學教會法、執業律師，後任杜林大學物理教授；1856 年過世。
- 卡爾斯魯厄會議 1860：S. Cannizzaro 散發 *Sunto di un corso di filosofia chimica*（1858），讓亞佛加厥假說被普遍接受、原子量統一。
- 「莫耳」Mol：W. Ostwald 於 1890 年代開始使用。
- 亞佛加厥常數命名：J. Perrin (1909) 以布朗運動量測並提議命名；2019 SI 定義 NA＝6.022 140 76 × 10²³ mol⁻¹（BIPM, *The International System of Units*, 9th ed.）。
- 戴維：1807 年電解熔融苛性鈉／苛性鉀得到金屬鈉、鉀（Bakerian Lecture, *Phil. Trans.* 98, 1808）；1810 年確認氯是元素。
- 鈉↔鹽：58.44 ÷ 22.99 ＝ 2.54；1800 mg × 2.54 ≈ 4.6 g；成人鈉上限 2400 mg/日（依國人 DRIs 現行版本）。

歌詞是對決誇飾（例如「論文放了 50 年沒人看到」），正確史實交給字卡；投票卡底部預設註明「歌詞為饒舌對決的誇飾，史實見字卡與說明欄｜本片影像與聲音由 AI 生成」。

## 怎麼做成影片（Colab，不需要本機顯卡）

前置（只做一次，見 workflow repo 的 `cloud/README.md`）：Google AI Pro（含 Colab 運算單元）或購買 Colab 單元；`uv tool install google-colab-cli`；`colab usage` 登入。

1. 把這個資料夾放進 workflow repo 的 `pipeline/` 底下，並補上範本的程式：
   ```bash
   git clone https://github.com/mathruffian-dot/shanshiba-workflow-colab.git
   cd shanshiba-workflow-colab
   cp -r pipeline/template_battle pipeline/mole_battle
   cp <本 repo>/rap_battle/mole_battle/battle.json pipeline/mole_battle/
   ```
2. 開機，在雲端用 YuE2 生歌：
   ```bash
   python cloud/colab_h3.py start
   python cloud/colab_h3.py film pipeline/mole_battle yue
   ```
   每人抽 10 首（seed 1–10），只留 144 BPM 的，再依逐句聽寫排序，第一名自動當成 `song/A.mp3`、`song/B.mp3`。
   **一定要自己聽 `out/yue/A/`、`out/yue/B/` 的候選**（排序在各自的 `pick.json`），挑的時候注意：
   - 數字（6.02、2.54、1800、1811）有沒有唸清楚；
   - 亞佛加厥的 4 句副歌（`[CHORUS]` 第一段）好不好聽；
   - 兩人聲音是否一低一高、聽得出是兩個人。

   想換成別首：把那首轉成 mp3 存成本機的 `pipeline/mole_battle/song/A.mp3`（或 `B.mp3`），下一次 `film` 會一起上傳。
   如果某人 10 首都不是 144 BPM，程式會停下來，多抽 10 首再跑：
   ```bash
   python cloud/colab_h3.py film pipeline/mole_battle yue --env YUE_SEEDS=11,12,13,14,15,16,17,18,19,20
   ```
3. 接著分段跑（每段都會把 `out/` 同步回本機，在本機看關卡）：
   ```bash
   python cloud/colab_h3.py film pipeline/mole_battle songs dj audio      # 聽 out/audio/mix.wav、看 out/song/songs_report.json
   python cloud/colab_h3.py film pipeline/mole_battle chars scenes frames # 看 out/chars/、out/first/_sheet.jpg
   python cloud/colab_h3.py film pipeline/mole_battle specs h3            # 看 out/review/clips_*.jpg
   python cloud/colab_h3.py film pipeline/mole_battle cut review srt      # 看完整成片 out/cut/莫耳之戰_v1_1920x1080.mp4
   python cloud/colab_h3.py stop                                          # 一定要關，閒置照扣單元
   ```
   範本實測整場約 1.5–2 小時、15–18 個運算單元（其中 `yue` 兩人各 10 首約 9 分鐘）。

   改用 Suno 的話：跳過 `yue`，把 `songtext/suno_*` 貼到 Suno 網頁 Create → Custom，挑好的歌存成 `song/A.mp3`、`song/B.mp3`。

**要注意的地方**

- 鏡頭時間（`at`）都綁在歌詞句子、DJ 口白和收尾拍上，不綁前奏長度：YuE2 幾乎沒有前奏時，範本會自動把音樂往後推、讓 DJ 口白塞得下，換場也不會撞鏡。若 `frames` 仍列出順序反掉或太短的鏡，照提示改那幾鏡的 `at`。
- YuE2 的段落照 14 版配方排好：每段 4 句，B 的第 16–17 句是 2 句的 `[PRE-CHORUS]`；B 最後殺招段 6 句會切成 4＋2 兩段 `[CHORUS]`。生出來的歌在第二段 `[CHORUS]` 前若有怪停頓，多抽幾首挑。
- YuE2 不一定有刷碟聲，攻擊性也比 Suno 弱；字幕、韻腳特效和字卡會補上「講清楚」的部分。
- 本機 Qwen 首幀畫不出側臉對峙：`V01`、`D01`、`D02`、`D03` 若要互瞪的構圖，把 `image_backend` 改 `"img25"`（要 OpenAI 金鑰），或拆成兩個單人鏡。
- 黑板、秤、筆記本上的字（`F04` HO、`F10` g → mol → N、`F11` 三個化學式、`F13` 4.6 g）若首幀畫成亂碼，刪那張 png 重畫；仍不行就把 `frame` 裡的字拿掉，靠字卡交代。
- 送去生歌的讀音已處理（YuE2、Suno 共用）：亞佛加厥數唱段寫成「亞佛加決數」、化學式拆成「H 二 O」「C H 二 O」、數字寫國字；字幕（`show`）用原字與阿拉伯數字。生完看 `songs_report.json` 的低分句，人工聽過再決定。
- 授權：Qwen-Image 2.1、Breeze TTS 2、YuE2 權重不可商用；MiniMax H3 授權排除美、歐盟、英、南韓（Colab 機房常在美國，請自行評估）。課堂非營利使用請在影片標示 AI 生成。
