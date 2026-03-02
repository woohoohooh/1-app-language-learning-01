import json
import glob

unique_words = set()

# Все .json в текущей папке
for file in glob.glob("*.json"):
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        words_list = data.get("words", [])
        for item in words_list:
            word = item.get("english")
            if word:
                unique_words.add(word.strip())

    except Exception as e:
        print(f"Error in {file}: {e}")

# Сортировка и сохранение
with open("words.txt", "w", encoding="utf-8") as out:
    for w in sorted(unique_words):
        out.write(w + "\n")

print(f"Saved {len(unique_words)} unique words to words.txt")
