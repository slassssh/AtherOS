@echo off
REM AtherOS Windows Executable Builder
REM Requires: pip install pyinstaller

echo [AtherOS] Building Windows executable...

pip install pyinstaller --quiet

pyinstaller ^
    --name atheros-api ^
    --onefile ^
    --console ^
    --add-data "backend;backend" ^
    --add-data "VERSION;." ^
    --add-data ".env.example;." ^
    --hidden-import backend.app.api.app ^
    --hidden-import backend.app.core.engine ^
    --hidden-import backend.app.memory.manager ^
    --hidden-import backend.app.cluster.manager ^
    --hidden-import uvicorn ^
    --hidden-import fastapi ^
    --hidden-import sqlalchemy ^
    --collect-all backend ^
    backend\app\main.py

echo.
echo [AtherOS] Build complete: dist\atheros-api.exe
echo [AtherOS] Run with: dist\atheros-api.exe
