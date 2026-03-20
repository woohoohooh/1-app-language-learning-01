import json
from pathlib import Path

JSON_DIR = Path(".")  # текущая папка

for json_file in JSON_DIR.glob("*.json"):
    print("Processing:", json_file.name)

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    changed = False

    if isinstance(data, dict) and "words" in data:
        # словарь с ключом "words"
        for word in data["words"]:
            if isinstance(word, dict):
                english_word = word.get("english", "").strip()
                if english_word and "audio" not in word:
                    folder_name = english_word.replace(" ", "_")
                    word["audio"] = [f"audio/{folder_name}/1.wav"]
                    changed = True

    elif isinstance(data, list):
        for i, item in enumerate(data):
            if isinstance(item, dict):
                english_word = item.get("english", "").strip()
                if english_word and "audio" not in item:
                    folder_name = english_word.replace(" ", "_")
                    item["audio"] = [f"audio/{folder_name}/1.wav"]
                    changed = True
            elif isinstance(item, str):
                # элемент списка — просто строка, превращаем в словарь
                folder_name = item.replace(" ", "_")
                data[i] = {
                    "english": item,
                    "audio": [f"audio/{folder_name}/1.wav"]
                }
                changed = True

    if changed:
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Updated JSON: {json_file.name}")

print("Готово")
