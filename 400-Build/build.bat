mkdir 000-Dist

cd 200-DesksetFront
call npm install
call npm run build
cd ..\

cd 300-DesksetBack
call uv sync
call python setup.py
cd ..\

copy 200-DesksetFront\src-tauri\target\debug\Deskset.exe 000-Dist
xcopy 300-DesksetBack\dist\DesksetBack 000-Dist /s
tar -czf Deskset.zip 000-Dist
