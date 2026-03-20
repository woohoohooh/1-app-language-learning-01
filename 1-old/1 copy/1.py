import os
import json

INPUT_DIR = "."
OUT_WORDS = "english/words"
OUT_PHRASES = "english/phrases"
OUT_SENTENCES = "english/sentences"

os.makedirs(OUT_WORDS, exist_ok=True)
os.makedirs(OUT_PHRASES, exist_ok=True)
os.makedirs(OUT_SENTENCES, exist_ok=True)


def normalize_id(text):
    return text.lower().replace(" ", "-").replace("_", "-")


def convert_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    theme = data.get("theme", "")
    level = data.get("level", "")
    words_data = data.get("words", [])

    out_words = []
    out_phrases = []
    out_sentences = []

    for w in words_data:
        base = w.get("english", "").strip()
        base_tr = w.get("translation", "").strip()

        # WORDS
        if base:
            out_words.append({
                "id": normalize_id(base),
                "english": base,
                "translation": base_tr,
                "audio": [f"audio/words/{base}.wav"]
            })

        # PHRASES
        ew = w.get("english_words", "").strip()
        tw = w.get("translation_words", "").strip()
        if ew:
            out_phrases.append({
                "id": normalize_id(ew),
                "english": ew,
                "translation": tw,
                "audio": [f"audio/phrases/{ew}.wav"]
            })

        # SENTENCES
        es = w.get("english_sentences", "").strip()
        ts = w.get("translation_sentences", "").strip()
        if es:
            out_sentences.append({
                "id": normalize_id(es),
                "english": es,
                "translation": ts,
                "audio": [f"audio/sentences/{es}.wav"]
            })

    def build_json(items):
        return {
            "theme": "Часто используемые слова",
            "level": level,
            "name": "Words",
            "items": items
        }

    base_name = os.path.splitext(os.path.basename(filepath))[0]

    def save(path, name, content):
        with open(os.path.join(path, name), "w", encoding="utf-8") as f:
            json.dump(content, f, ensure_ascii=False, indent=2)

    save(OUT_WORDS, base_name + "_words.json", build_json(out_words))
    save(OUT_PHRASES, base_name + "_phrases.json", build_json(out_phrases))
    save(OUT_SENTENCES, base_name + "_sentences.json", build_json(out_sentences))

    print(f"OK: {filepath} -> {len(out_words)} words, {len(out_phrases)} phrases, {len(out_sentences)} sentences")


def main():
    for file in os.listdir(INPUT_DIR):
        if file.endswith(".json"):
            convert_file(file)


if __name__ == "__main__":
    main()
