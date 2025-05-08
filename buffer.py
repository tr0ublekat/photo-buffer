#!env/Scripts/python

import datetime
import subprocess
import os
import keyboard
import threading

paths = {
    1: r"D:\education\sem6\lections\network\images",
    2: r"C:\Users\tr0ublekat\Desktop"
}
current_path = None


def get_path():
    global current_path
    print("Выберите путь для сохранения изображений:")
    for path in paths:
        print(str(path) + ": " + paths[path])

    current_path = paths[int(input("Введите номер пути: "))]
    print(f"Путь для сохранения изображений: {current_path}")


def check_device_connected():
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
    return 'device' in result.stdout


def get_photo(index=1):
    try:
        output = subprocess.check_output(
            ['adb', 'shell', 'ls', '-t', '/sdcard/DCIM/Camera'],
            text=True,
            stderr=subprocess.STDOUT
        ).splitlines()
        return output[index-1].strip() if output else None
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при получении списка файлов: {e.output}")
        return None


def download_file(remote_path, local_path):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        file_extension = os.path.splitext(remote_path)[1]  # Получаем расширение файла
        new_name = f"{timestamp}{file_extension}"
        local_path = os.path.join(local_path, new_name)

        subprocess.run(['adb', 'pull', remote_path, local_path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при скачивании файла: {e}")
        return False


def main(index=1):
    if not check_device_connected():
        print("Устройство не найдено. Подключите телефон по USB и включите отладку.")
        return

    photo = get_photo(index=index)
    if not photo:
        print("Не удалось найти фотографии в /sdcard/DCIM/Camera")
        return

    remote_path = f"/sdcard/DCIM/Camera/{photo}"

    if not download_file(remote_path, current_path):
        return


if __name__ == "__main__":
    keyboard.add_hotkey('ctrl+space', main)
    keyboard.add_hotkey('ctrl+shift+1', main, args=(1,))
    keyboard.add_hotkey('ctrl+shift+2', main, args=(2,))
    keyboard.add_hotkey('ctrl+shift+3', main, args=(3,))
    keyboard.add_hotkey('ctrl+shift+4', main, args=(4,))
    keyboard.add_hotkey('ctrl+shift+5', main, args=(5,))
    keyboard.add_hotkey('ctrl+shift+6', main, args=(6,))
    keyboard.add_hotkey('ctrl+shift+7', main, args=(7,))
    keyboard.add_hotkey('ctrl+shift+8', main, args=(8,))
    keyboard.add_hotkey('ctrl+shift+9', main, args=(9,))
    keyboard.add_hotkey('ctrl+shift+space', lambda: os._exit(0))
    print("Ctrl+Shift+<number> для копирования <number> фотографии с конца.")
    print("Ctrl+Space для копирования последней фотографии.")

    try:
        get_path()
        keyboard.wait()
    except KeyboardInterrupt:
        print("Программа завершена.")
        exit(0)