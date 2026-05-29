@echo off
chcp 65001 >nul
title 考研复习系统 - 一键启动

echo ============================================
echo    📚 考研知识点复习系统
echo    正在启动...
echo ============================================
echo.

:: 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未检测到 Python，请先安装 Python 3.10+
    echo    下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: 检查依赖
echo 📦 检查依赖...
pip install -r requirements.txt -q
if %errorlevel% neq 0 (
    echo ⚠️ 部分依赖安装失败，尝试继续...
)

:: 启动桌面应用
echo.
echo ✅ 启动中...
start "" python desktop_app.py

:: 等待几秒后打开浏览器（备用）
timeout /t 3 /nobreak >nul
start http://127.0.0.1:5000

echo.
echo ============================================
echo    ✅ 应用已启动！
echo    桌面窗口应已弹出
echo    如果没有，请访问 http://127.0.0.1:5000
echo ============================================
pause
