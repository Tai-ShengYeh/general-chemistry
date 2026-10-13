# W05–W16 錨點概念短片

本批次補齊 12 個**教學週**。課程總覽採「16 教學週 + 2 考試週」；W09 是化學鍵教學週，不是期中考。總覽中獨立的期中考、期末考列沒有建立影片。W01–W04 的檔案不變。

每週資料夾提供：

- `<slug>_animation.mp4`：1280 × 720、24 fps、H.264 / AAC、完整繁體中文字幕燒錄於畫面。
- `<slug>_animation.srt`：可下載的完整逐句旁白字幕。
- `<slug>_animation.vtt`：HTML 原生字幕軌。因影片已有字幕，原生軌預設不開啟，避免雙重字幕；可由播放器選用。
- `poster.jpg`、`storyboard.json`、`narration.txt`、`make_narration.ps1`、`render_animation.py`。

影片放在各週第三張錨點投影片之後。影片控制項不觸發翻頁；離開投影片時暫停。閱讀模式採單欄，保留既有課文及行動版樣式。

## 重新製作

需要 Python + Pillow、ffmpeg / ffprobe，以及 WSL 可呼叫的 Windows PowerShell、`Microsoft Hanhan Desktop` 繁體中文語音。預設使用 Windows 微軟正黑體；可用 `CHEM_FONT`、`CHEM_BOLD` 指定其他含完整中文字形的字型。

```bash
python docs/animations/w16_redox/render_animation.py
python docs/animations/validate_week_animations.py
```

共用 `render_teaching_animation.py` 逐句合成語音，以實際 WAV 長度安排圖卡與 SRT / VTT；結尾保留至少兩秒，不使用 `-shortest` 截斷。圖卡使用量測寬度的換行／字體縮放。語音快取依完整句子內容失效，不沿用不同版本的旁白。

`narration.wav`、`.render-cache/`、`__pycache__/` 都是被忽略的中間檔，不上傳。PowerShell 的 `-ExecutionPolicy Bypass` 只作用於此受信任指令碼的當次程序，不變更機器的持續性政策。

## 驗證紀錄

- `w05-w16-validation.json`：12 支影片的 ffprobe 音／畫長度、影格數、檔案大小、完整 ffmpeg 解碼、字幕內容與時間覆蓋、所有相對資源連結。
- `w05-w16-browser-validation.json`：本機 HTTP 服務上的實際 Chromium 播放、VTT 8 句載入、控制項點擊／鍵盤不翻頁、隱藏影片暫停、390 px 手機單欄測試。
- 已檢視每支影片開場、中段與結尾實際影格，共 36 張；字型字元表檢查未缺字。
- 以 Git 原始版本比較，各週既有 `<section>` 內容均保留；新投影片只插入第三張之後。24 個 inline JavaScript 區塊通過 Node 語法檢查。

## 範圍與限制

這些是約一分鐘多的概念短片與流程圖逐步揭露，不是完整課程錄影或分子三維模擬；需搭配原有例題與講解。英文名詞採系統語音，發音可能較生硬。食品法規與製程數值須在教學前核對現行規定，影片明確不把 pH 4.6 當成單獨的安全保證。

W13 原始課文在 390 px 閱讀模式即有全頁水平溢出（原始版本實測寬度 414 px）；本次影片本身無水平溢出，未改動該既有課文排版問題。

本批次由 PR 審查，尚未合併；公開 GitHub Pages 不會在 PR 建立時立即更新。
