#include <windows.h>
#include <initguid.h>  // 包含在 olectl.h 之前，来让系统定义 IID_IPicture
#include <olectl.h>
#include <shellapi.h>

// 代码来源：https://stackoverflow.com/questions/2289894/how-can-i-save-hicon-to-an-ico-file
HRESULT SaveIcon(HICON hIcon, const wchar_t* path) {
    // Create the IPicture intrface
    PICTDESC desc = { sizeof(PICTDESC) };
    desc.picType = PICTYPE_ICON;
    desc.icon.hicon = hIcon;
    IPicture* pPicture = 0;
    HRESULT hr = OleCreatePictureIndirect(&desc, IID_IPicture, FALSE, (void**)&pPicture);
    if (FAILED(hr)) return hr;

    // Create a stream and save the image
    IStream* pStream = 0;
    CreateStreamOnHGlobal(0, TRUE, &pStream);
    LONG cbSize = 0;
    hr = pPicture->SaveAsFile(pStream, TRUE, &cbSize);

    // Write the stream content to the file
    if (!FAILED(hr)) {
        HGLOBAL hBuf = 0;
        GetHGlobalFromStream(pStream, &hBuf);
        void* buffer = GlobalLock(hBuf);
        // 显式指定 CreateFileW...否则编译出错
        HANDLE hFile = CreateFileW(path, GENERIC_WRITE, 0, 0, CREATE_ALWAYS, 0, 0);
        if (!hFile) hr = HRESULT_FROM_WIN32(GetLastError());
        else {
            DWORD written = 0;
            WriteFile(hFile, buffer, cbSize, &written, 0);
            CloseHandle(hFile);
        }
        GlobalUnlock(buffer);
    }
    // Cleanup
    pStream->Release();
    pPicture->Release();
    return hr;
}

HICON GetIcon(const LPCWSTR filePath) {
    SHFILEINFOW sfi = {0};

    if (SHGetFileInfoW(filePath, 0, &sfi, sizeof(sfi), SHGFI_ICON | SHGFI_LARGEICON)) {
        return sfi.hIcon;
    } else {
        return NULL;
    }
}

int main() {
    HICON hIcon = GetIcon(L".\\main.cpp");
    if (!hIcon) return -1;
    SaveIcon(hIcon, L".\\icon.png");
    return 0;
}
