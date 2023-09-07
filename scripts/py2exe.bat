@echo off

:: set path 
set ROOT=%~dp0..\
set PATH=%ROOT%\\.venv\\Scripts\\pyinstaller.exe
set FILE=%ROOT%\\lazylogger.py

:: run 
%PATH% --onefile --noconsole %FILE%