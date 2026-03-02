import os, json, re

JSON_FOLDER = "."
AUDIO_FOLDER = "current audio"
OUTPUT_FILE = "missing_phrases.txt"

def normalize_phrase(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")

# список аудио файлов
audio_files = [f.lower() for f in os.listdir(AUDIO_FOLDER) if f.endswith(".wav")]

missing = []

for fn in os.listdir(JSON_FOLDER):
    if not fn.endswith(".json"):
        continue

    with open(fn, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data.get("items", []):
        eng = item.get("english")
        if not eng:
            continue

        norm = normalize_phrase(eng)

        # проверяем вхождение
        found = any(norm in a for a in audio_files)

        if not found:
            missing.append(eng)

missing = sorted(set(missing))

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(missing))

print("Missing:", len(missing))
