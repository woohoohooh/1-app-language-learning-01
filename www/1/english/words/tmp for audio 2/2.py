import os
import json
from collections import Counter

def check_duplicates_in_directory(directory="."):
    print(f"Scanning directory: {os.path.abspath(directory)}\n")

    for filename in os.listdir(directory):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(directory, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[ERROR] Could not read {filename}: {e}")
            continue

        items = data.get("items", [])
        english_words = []

        for item in items:
            english = item.get("english")
            if english:
                english_words.append(english.strip().lower())

        counter = Counter(english_words)
        duplicates = {word: count for word, count in counter.items() if count > 1}

        if duplicates:
            print(f"⚠ Duplicates found in: {filename}")
            for word, count in duplicates.items():
                print(f"   - '{word}' appears {count} times")
            print()
        else:
            print(f"✓ No duplicates in: {filename}")

if __name__ == "__main__":
    check_duplicates_in_directory()