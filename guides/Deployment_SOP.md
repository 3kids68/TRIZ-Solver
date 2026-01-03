# TRIZ Solver GitHub Pages 部署 SOP

> **目標**：將 TRIZ Solver 部署到 GitHub Pages，讓任何人都可以透過網址直接使用，無需安裝任何軟體。

---

## 📋 前置準備

### 需要的東西
1. ✅ 一個 GitHub 帳號（免費）
2. ✅ 專案的 `docs/` 資料夾（已經準備好）
3. ✅ 瀏覽器（Chrome、Edge、Firefox 皆可）

### 不需要的東西
- ❌ 不需要懂程式碼
- ❌ 不需要安裝 Git 軟體
- ❌ 不需要使用命令列

---

## 🚀 部署步驟

### 步驟 1：建立 GitHub 帳號

如果您已經有 GitHub 帳號，請跳到步驟 2。

1. 前往 [https://github.com](https://github.com)
2. 點擊右上角 **Sign up** 按鈕
3. 填寫：
   - **Email**：您的電子郵件
   - **Password**：設定密碼
   - **Username**：選擇一個使用者名稱（這會出現在網址中）
4. 完成驗證後，點擊 **Create account**
5. 到您的信箱收取驗證信，點擊連結完成驗證

---

### 步驟 2：建立新的 Repository（儲存庫）

1. 登入 GitHub 後，點擊右上角的 **+** 號，選擇 **New repository**

2. 填寫以下資訊：
   - **Repository name**：輸入 `TRIZ-Solver`（可自訂，但建議用英文）
   - **Description**：輸入 `AI-Assisted TRIZ Engineering Problem Solver`
   - **Public / Private**：選擇 **Public**（公開，才能使用 GitHub Pages）
   - **Initialize this repository**：不要勾選任何選項

3. 點擊綠色按鈕 **Create repository**

---

### 步驟 3：上傳專案檔案

#### 方法 A：使用網頁上傳（推薦，最簡單）

1. 在新建立的 Repository 頁面，您會看到 **Quick setup** 指引

2. 點擊 **uploading an existing file** 連結

3. 將整個 `docs` 資料夾的**所有內容**拖曳到上傳區域：
   ```
   docs/
   ├── index.html
   ├── .nojekyll
   ├── data/
   │   ├── parameters.json
   │   ├── principles.json
   │   └── matrix.json
   ├── css/
   │   └── style.css
   └── js/
       ├── engine.js
       └── main.js
   ```

   > ⚠️ **重要**：請上傳 `docs` 資料夾**裡面的檔案**，不要上傳 `docs` 資料夾本身。
   > 
   > 正確的結構應該是：
   > - ✅ `index.html` 在根目錄
   > - ✅ `data/` 資料夾在根目錄
   > - ❌ 不是 `docs/index.html`

4. 在下方 **Commit changes** 區域：
   - 輸入訊息：`Initial commit - TRIZ Solver`
   - 點擊綠色按鈕 **Commit changes**

5. 等待上傳完成（可能需要幾秒鐘）

---

### 步驟 4：啟用 GitHub Pages

1. 在 Repository 頁面，點擊上方的 **Settings**（齒輪圖示）

2. 在左側選單中，找到並點擊 **Pages**

3. 在 **Source** 區域：
   - **Branch**：選擇 `main`（或 `master`）
   - **Folder**：選擇 `/ (root)`
   - 點擊 **Save** 按鈕

4. 頁面會重新整理，並顯示：
   ```
   Your site is ready to be published at https://<username>.github.io/TRIZ-Solver/
   ```

5. 等待 1-2 分鐘讓 GitHub 建置網站

---

### 步驟 5：驗證部署成功

1. 點擊步驟 4 中顯示的網址，例如：
   ```
   https://your-username.github.io/TRIZ-Solver/
   ```

2. 您應該會看到 TRIZ Solver 的網頁介面

3. 測試功能：
   - ✅ 在 Step 1 輸入系統名稱，點擊 Next
   - ✅ 在 Step 2 輸入改善參數（例如：`faster`），點擊 🔍
   - ✅ 輸入惡化參數（例如：`hot`），點擊 🔍
   - ✅ 點擊 **Generate Solution** 查看結果

4. 如果一切正常，恭喜！您已成功部署 🎉

---

## 🔧 常見問題排解

### Q1: 網頁顯示 404 Not Found
**原因**：GitHub Pages 尚未建置完成，或檔案結構不正確。

**解決方法**：
1. 等待 5 分鐘後重新整理
2. 確認 `index.html` 在 Repository 的根目錄（不是在 `docs/` 資料夾內）
3. 到 Settings > Pages 確認 Source 設定為 `main` 和 `/ (root)`

---

### Q2: 網頁顯示但樣式跑掉
**原因**：CSS 或 JS 檔案路徑錯誤。

**解決方法**：
1. 按 F12 打開瀏覽器開發者工具
2. 查看 Console 是否有錯誤訊息
3. 確認 `css/style.css` 和 `js/` 資料夾都有正確上傳

---

### Q3: 點擊 🔍 按鈕沒有反應
**原因**：JavaScript 引擎尚未載入完成，或資料檔案載入失敗。

**解決方法**：
1. 打開瀏覽器開發者工具（F12）
2. 查看 Console 是否有錯誤訊息
3. 確認 `data/` 資料夾內的 3 個 JSON 檔案都有上傳
4. 重新整理頁面，等待左側 Log 顯示 "Engine ready"

---

### Q4: 想要更新網站內容
**方法**：
1. 到 Repository 頁面
2. 點擊要修改的檔案
3. 點擊右上角的鉛筆圖示（Edit）
4. 修改內容後，點擊 **Commit changes**
5. 等待 1-2 分鐘，網站會自動更新

---

## 📤 分享您的網站

部署成功後,您可以將網址分享給任何人：

```
https://<your-username>.github.io/TRIZ-Solver/
```

他們只需要用瀏覽器打開連結，就可以直接使用 TRIZ Solver，無需安裝任何軟體！

---

## 🎯 進階選項（可選）

### 使用自訂網域名稱

如果您有自己的網域（例如 `triz.example.com`）：

1. 到 Settings > Pages
2. 在 **Custom domain** 輸入您的網域
3. 到您的網域註冊商設定 DNS：
   - 類型：`CNAME`
   - 名稱：`triz`（或您想要的子網域）
   - 值：`<your-username>.github.io`

---

## 📞 需要協助？

如果遇到問題：
1. 檢查瀏覽器 Console（F12）的錯誤訊息
2. 確認所有檔案都已正確上傳
3. 參考 GitHub Pages 官方文件：[https://pages.github.com](https://pages.github.com)

---

**祝您部署順利！** 🚀
