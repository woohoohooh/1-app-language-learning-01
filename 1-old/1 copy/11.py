import os
import json

ROOT_DIR = "."


def clean_items_audio(data):
    # Проверяем, что это именно твой формат
    if not isinstance(data, dict):
        return False

    if "items" not in data or not isinstance(data["items"], list):
        return False

    changed = False
    for item in data["items"]:
        if isinstance(item, dict) and "audio" in item:
            del item["audio"]
            changed = True

    return changed


def process_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        return  # пропускаем битые или не JSON

    changed = clean_items_audio(data)

    if not changed:
        return  # не трогаем чужие JSON

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✔ cleaned {path}")


def main():
    for root, _, files in os.walk(ROOT_DIR):
        for name in files:
            if name.endswith(".json"):
                process_file(os.path.join(root, name))


if __name__ == "__main__":
    main()
