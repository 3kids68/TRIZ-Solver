# AI-Assisted TRIZ Solver

這是一個基於 **TRIZ (發明問題解決理論)** 的 AI 輔助工程解決方案引擎。它引導工程師將模糊的技術問題轉化為標準矛盾參數，並提供創新發明原則建議。

> **🌐 線上版本 (Online Demo)**
> 本專案支援 GitHub Pages，可直接在瀏覽器使用：
> [前往 GitHub Pages 網站](https://<your-username>.github.io/TRIZ-Solver/) (部署後可用)

---

## 📂 專案結構 (Directory Structure)

基於 MECE 原則整理，本專案分為以下三個主要區塊：

1.  **guides/** - **文件與手冊**
    *   📖 [Deployment_SOP.md](guides/Deployment_SOP.md): 詳細的 GitHub Pages 部署圖文教學。
    *   ⚡ [Deployment_QuickRef.md](guides/Deployment_QuickRef.md): 快速部署與檢查清單。
    *   ⚙️ [Technical_Specs.md](guides/Technical_Specs.md): 系統架構與技術規格書 (TRD)。
2.  **docs/** - **靜態網頁 (GitHub Pages)**
    *   這是為了 GitHub Pages 部署所準備的純前端版本，包含 HTML/CSS/JS 和所有 JSON 資料庫。
    *   **不要**手動修改這裡的自動生成檔案，除非您是在維護前端版本。
3.  **src/** - **Python 原始碼**
    *   包含 FastAPI 後端與演算法核心（如欲進行 Python 開發或修改演算法，請由此處著手）。
    *   `app.py`: FastAPI 伺服器入口。
    *   `main.py`: 命令行 (CLI) 版本入口。

---

## 🚀 如何使用 (Usage)

本系統提供兩種執行模式，請依需求選擇：

### 模式 A：網頁瀏覽器版 (推薦 for Users)
無需安裝 Python，部署到 GitHub Pages 後即可隨處使用。
*   **部署方法**：請參閱 `guides/Deployment_SOP.md`。
*   **適用場景**：最終用戶、團隊分享、展示。

### 模式 B：本地 Python 開發版 (推薦 for Developers)
如果您需要修改演算法、擴充知識庫或進行二次開發。

1.  **安裝依賴**
    ```powershell
    pip install -r requirements.txt
    ```

2.  **啟動 Web Server**
    ```powershell
    uvicorn app:app --reload --port 8000
    ```
    啟動後訪問：`http://localhost:8000/static/index.html`

3.  **啟動命令行版 (CLI)**
    ```powershell
    python main.py
    ```

---

## 🛠️ 維護指南

### 修改知識庫 (JSON)
如果您需要新增或修改 TRIZ 參數、發明原則：
1.  編輯 `docs/data/` (如果是為了線上版) 或 `src/data/` (如果是為了 Python 版) 下的 JSON 檔案。
2.  **注意**：為了保持一致，建議修改後同步更新兩個資料夾。

### 修改前端介面
1.  編輯 `docs/index.html`、`docs/css/style.css` 或 `docs/js/main.js`。
2.  推送到 GitHub 即可自動更新線上版本。

---

<footer style="text-align: center; margin-top: 50px; color: #888;">
    Developed by Wesley Chang @2026
</footer>
