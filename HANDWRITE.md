# 普通化學手寫動畫

課程首頁及每週進度表增加手寫動畫入口。每個投影片保留原有內容與原頁碼，在封面及閱讀工具列增加動畫連結，末尾加一張章節選單。

涵蓋W01–W16與W01b、W02b兩個延伸單元。W01b沿用既有6章，其餘每單元2章，共40章、304幕、93個作答停頓。新增34章採短句繁體中文與少量越南語關鍵詞，每章兩個題目停頓，解答放下一幕。

網站入口：`docs/handwrite/index.html`。各章可播放、暫停、拖曳、調速、切幕與重播；旁白MP3與字型隨教材附上。這次交付為互動HTML，沒有額外輸出MP4。原課程已有的錨點影片與因次分析練習繼續保留。

## 維護

編輯`docs/handwrite/*.lesson.json`作為教材腳本。完整製作工作區另外保存課程作者腳本、來源快照與配音快取；播放器來源技能保持原先的private設定。

本機整合器使用與repo同層的`general-chemistry-handwrite/`，將完成的旁白播放器複製到docs。只有明確列出的執行時檔案、可編輯腳本及授權檔會發布；原始TTS快取、ZIP、教師專用題庫與私有技能原始碼不隨網站上傳。

```powershell
python -X utf8 tools/integrate_handwrite.py
python -X utf8 tools/check_handwrite.py
python -X utf8 tools/check_handwrite.py --base https://tai-shengyeh.github.io/general-chemistry/
```

整合器只修改標記區塊，先移除舊標記再核對原投影片SHA256；若原始教材已被其他人修改，會停止以便更新來源快照，而不是覆寫新教材。標準模式要求40章都有正式旁白；`--preview`只供發布前測試。

驗收包含原始翻頁、解答先隱藏後揭露、手機閱讀模式、投影與橫向小螢幕、章節導覽、音訊實際播放前進、seek、速度、重設與作答門檻。版面微調只增加閱讀模式雙欄子元素的寬度上限，修正原W13寬圖超出手機視窗的問題。

科學條件、例題與來源見`docs/handwrite/teacher-notes.md`及`source-map.md`。保留原課程OpenStax來源與字型／播放器授權。
