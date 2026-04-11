import ctypes

from pathlib import Path
import imghdr

SUPPORT_TYPE = ['png', 'jpg', 'jpeg']


def set_wallpaper(image_path):
    if not Path(image_path).is_file():
        raise FileExistsError(f'{image_path} 文件不存在！')
    if imghdr.what(image_path) not in SUPPORT_TYPE:
        raise TypeError(f'{image_path} 不是图片或格式不受支持！')

    image_path_buffer = ctypes.create_unicode_buffer(image_path)  # 明确指定 c_wchar

    # 0x0014 = SPI_SETDESKWALLPAPER
    # 0x0002 = SPIF_SENDCHANGE = SPIF_SENDWININICHANGE
    ctypes.windll.user32.SystemParametersInfoW(0x0014, 0, image_path_buffer, 0x0002)


if __name__ == '__main__':
    set_wallpaper('')
