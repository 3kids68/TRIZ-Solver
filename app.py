import sys
import os
import threading
import time
import webbrowser
from fastapi import FastAPI, HTTPException, Body, File
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional

# 內部模組
from src.engine import TRIZEngine
from src.models import SolutionReport, EngineeringParameter

# --- 資源路徑處理 (關鍵：支援 PyInstaller) ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

app = FastAPI(title="TRIZ Solver API")

# Initialize Engine with correct Data Path
DATA_DIR = resource_path(os.path.join('src', 'data'))
engine = TRIZEngine(data_dir=DATA_DIR)

# Mount Static Files (Frontend) with correct Path
static_dir = resource_path("static")
if not os.path.isdir(static_dir):
    # Fallback for dev mode context
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

class NormalizeRequest(BaseModel):
    text: str

class SolveRequest(BaseModel):
    improving_id: int
    worsening_id: int

from fastapi.responses import RedirectResponse

@app.get("/")
def read_root():
    return RedirectResponse(url="/static/index.html")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(resource_path("static/favicon.ico")) if os.path.exists(resource_path("static/favicon.ico")) else None

@app.post("/api/normalize")
def normalize_input(req: NormalizeRequest):
    match, logs = engine.normalize_input_to_parameter(req.text)
    return {
        "match": match,
        "logs": logs
    }

@app.post("/api/solve", response_model=SolutionReport)
def solve_contradiction(req: SolveRequest):
    try:
        report = engine.solve_contradiction(req.improving_id, req.worsening_id)
        return report
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import multiprocessing
    import uvicorn
    
    # 支援 PyInstaller 的多程序啟動
    multiprocessing.freeze_support()
    
    # 自動開啟瀏覽器
    def open_browser():
        time.sleep(1.5)
        webbrowser.open("http://127.0.0.1:8000/static/index.html")
    
    # 啟動瀏覽器執行緒
    threading.Thread(target=open_browser, daemon=True).start()
    
    # 啟動伺服器
    print("Starting TRIZ Solver Server on http://127.0.0.1:8000...")
    # workers=1 避免 PyInstaller 打包時的多程序問題
    # log_config=None 避免在 --noconsole 模式下報錯
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error", log_config=None)
