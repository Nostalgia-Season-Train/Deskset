mkdir 000-Dist

cd 200-DesksetFront
call npm install
call npm run build
cd ..\

cd 300-DesksetBack
call uv sync
call python setup.py
cd ..\

copy 200-DesksetFront\src-tauri\target\release\Deskset.exe 000-Dist
xcopy 350-DesksetBack.MCP\dist\DesksetBack 000-Dist /s
@REM tar -czf Deskset.tar -C 000-Dist .
powershell -Command "Compress-Archive -Path '000-Dist\*' -DestinationPath 'Deskset.MCP.zip'"
