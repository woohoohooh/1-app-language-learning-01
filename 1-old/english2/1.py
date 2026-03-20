import json
import os
from pathlib import Path

JSON_DIR = ""
AUDIO_ROOT = "audio"

os.makedirs(AUDIO_ROOT, exist_ok=True)

for json_file in Path(JSON_DIR).glob("*.json"):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    changed = False

    for word in data.get("words", []):
        english_word = word.get("english", "").strip()
        if not english_word:
            continue

        folder_name = english_word.replace(" ", "_")
        folder_path = os.path.join(AUDIO_ROOT, folder_name)
        audio_path = os.path.join(folder_path, "1.wav")

        # создать папку
        os.makedirs(folder_path, exist_ok=True)

        # создать пустой 1.wav, если нет
        if not os.path.exists(audio_path):
            open(audio_path, "wb").close()

        # прописать в json, если нет audio
        if "audio" not in word:
            word["audio"] = [f"{AUDIO_ROOT}/{folder_name}/1.wav"]
            changed = True

    if changed:
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

print("Готово")
