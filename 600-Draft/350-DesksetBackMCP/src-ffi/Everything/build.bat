gcc -fPIC -shared "./main.c" -o "../../deskset/feature/search/everything/EverythingMain.dll"^
    -I "./sdk/include"^
    -L "./sdk/lib/" "./sdk/lib/Everything64.lib"

copy "./Everything64.dll" "../../deskset/feature/search/everything/Everything64.dll"

pause
