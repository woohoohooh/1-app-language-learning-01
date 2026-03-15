import os
import json
import re

folder = os.path.dirname(os.path.abspath(__file__))

for filename in os.listdir(folder):
    if not filename.endswith(".json"):
        continue

    path = os.path.join(folder, filename)

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"\nОшибка чтения JSON: {filename} -> {e}")
        continue

    objects = data if isinstance(data, list) else [data]

    for obj in objects:
        if not isinstance(obj, dict):
            continue

        items = obj.get("items", [])

        for item in items:
            if not isinstance(item, dict):
                continue

            original = item.get("original", "")
            english = item.get("english", "")

            if not re.search(rf"\b{re.escape(original)}\b", english, re.IGNORECASE):
                print(f"\nФайл: {filename}")
                print(f"original: {original}")
                print(f"english: {english}")
