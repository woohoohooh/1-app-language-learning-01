import os
from pathlib import Path
import shutil

# текущая папка (audio/)
BASE_DIR = Path("")
for wav_file in BASE_DIR.glob("*.wav"):
    # имя файла без расширения
    folder_name = wav_file.stem.replace(" ", "_")
    folder_path = BASE_DIR / folder_name

    # создаём папку
    folder_path.mkdir(exist_ok=True)

    # новый путь для файла
    new_file_path = folder_path / "1.wav"

    # перемещаем и переименовываем
    shutil.move(str(wav_file), str(new_file_path))

    print(f"{wav_file.name} → {new_file_path}")

print("Готово")
