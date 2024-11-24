@echo off
echo Starting Image Tools...

:: 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    pause
    exit /b 1
)

:: 检查依赖
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
)

:: 运行程序
python main.py

if errorlevel 1 (
    echo Program exited with error
    pause
    exit /b 1
)

exit /b 0