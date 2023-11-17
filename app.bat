@echo off
setlocal
    python -m shiny run --port 5000 --host localhost --reload app.py
endlocal