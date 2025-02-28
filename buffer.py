#!venv/Scripts/python

import subprocess
import os
from PIL import Image
import win32clipboard
from io import BytesIO
import keyboard
import threading
import time

def check_device_connected():
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
    return 'device' in result.stdout

def get_latest_photo():
    try:
        output = subprocess.check_output(
            ['adb', 'shell', 'ls', '-t', '/sdcard/DCIM/Camera'],
            text=True,
            stderr=subprocess.STDOUT
        ).splitlines()
        return output[0].strip() if output else None
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при получении списка файлов: {e.output}")
        return None

def download_file(remote_path, local_path):
    try:
        subprocess.run(['adb', 'pull', remote_path, local_path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при скачивании файла: {e}")
        return False

def copy_image_to_clipboard(image_path):
    try:
        with Image.open(image_path) as img:
            output = BytesIO()
            img.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]
            output.close()

            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()
            print("Изображение скопировано в буфер обмена!")
    except Exception as e:
        print(f"Ошибка при копировании: {e}")

def main():
    if not check_device_connected():
        print("Устройство не найдено. Подключите телефон по USB и включите отладку.")
        return

    latest_photo = get_latest_photo()
    if not latest_photo:
        print("Не удалось найти фотографии в /sdcard/DCIM/Camera")
        return

    remote_path = f"/sdcard/DCIM/Camera/{latest_photo}"
    local_path = os.path.join(os.getcwd(), f"temp_photo_{time.time()}.jpg")

    if not download_file(remote_path, local_path):
        return

    copy_image_to_clipboard(local_path)

    try:
        os.remove(local_path)
    except Exception as e:
        print(f"Ошибка при удалении временного файла: {e}")

def trigger_main():
    thread = threading.Thread(target=main)
    thread.start()

if __name__ == "__main__":
    keyboard.add_hotkey('ctrl+space', trigger_main)
    print("Программа запущена. Нажимайте Ctrl+Space для копирования последней фотографии.")
    keyboard.wait()