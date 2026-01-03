# TRIZ Solver Packaging Script

# 建議在虛擬環境中執行
# .\.venv\Scripts\Activate.ps1

Write-Host "--- Packaging TRIZ Web Solver (FastAPI) ---" -ForegroundColor Cyan
# 使用 --onedir (預設) 取代 --onefile 以降低被防火牆誤判為病毒的機率
& ".\.venv\Scripts\pyinstaller.exe" --name="TRIZ_Web_Solver" --onedir --noconsole --noconfirm --add-data "src/data;src/data" --add-data "static;static" --clean app.py

Write-Host "--- Packaging TRIZ CLI Solver (Rich) ---" -ForegroundColor Cyan
& ".\.venv\Scripts\pyinstaller.exe" --name="TRIZ_CLI_Solver" --onedir --noconfirm --add-data "src/data;src/data" --clean main.py


Write-Host "Cleaning up temporary build files..." -ForegroundColor Yellow
if (Test-Path "build") { Remove-Item -Recurse -Force build }
if (Test-Path "*.spec") { Remove-Item -Force *.spec }

Write-Host "Compressing output folders into ZIP files..." -ForegroundColor Cyan
# 為了方便傳輸且避免執行檔直接被掃描，將資料夾壓縮成 ZIP
if (Test-Path "dist/TRIZ_Web_Solver") {
    if (Test-Path "dist/TRIZ_Web_Solver_Package.zip") { Remove-Item "dist/TRIZ_Web_Solver_Package.zip" }
    Compress-Archive -Path "dist/TRIZ_Web_Solver" -DestinationPath "dist/TRIZ_Web_Solver_Package.zip"
}
if (Test-Path "dist/TRIZ_CLI_Solver") {
    if (Test-Path "dist/TRIZ_CLI_Solver_Package.zip") { Remove-Item "dist/TRIZ_CLI_Solver_Package.zip" }
    Compress-Archive -Path "dist/TRIZ_CLI_Solver" -DestinationPath "dist/TRIZ_CLI_Solver_Package.zip"
}

Write-Host "Packaging Complete! Check the 'dist' folder for ZIP files." -ForegroundColor Green

