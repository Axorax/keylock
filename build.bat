@echo off

pyinstaller ^
    --name="keylock" ^
    --onefile ^
    --strip ^
    --paths=env\Lib\site-packages ^
    --add-data="assets;assets" ^
    --noconsole ^
    --icon=assets/icon.ico ^
    --exclude-module numpy ^
    main.py
