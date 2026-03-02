import os
import json
import re

# ===== PATHS =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENGLISH_DIR = os.path.join(BASE_DIR, "english old", "words")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
OUT_FILE = os.path.join(BASE_DIR, "1-new-words.txt")

# True = только single word (без пробелов и дефисов)
# False = включая decision-maker, carry out, work-life balance
ONLY_SINGLE_WORD = True


# ===== AUDIO NORMALIZER =====
def normalize_audio(name: str) -> str:
    name = name.lower()

    # remove performer suffix: _kore, _john123
    name = re.sub(r"_[a-z0-9]+$", "", name)

    # underscore -> space
    name = name.replace("_", " ")

    # collapse spaces
    name = re.sub(r"\s+", " ", name)

    return name.strip()


# ===== LOAD AUDIO WORDS =====
def load_audio_words():
    words = set()
    if not os.path.exists(AUDIO_DIR):
        return words

    for f in os.listdir(AUDIO_DIR):
        if f.lower().endswith(".wav"):
            base = f[:-4]
            words.add(normalize_audio(base))

    return words


# ===== LOAD JSON WORDS (english only) =====
def load_json_words():
    words = set()
    if not os.path.exists(ENGLISH_DIR):
        return words

    for file in os.listdir(ENGLISH_DIR):
        if not file.endswith(".json"):
            continue

        path = os.path.join(ENGLISH_DIR, file)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue  # skip broken json

        if not isinstance(data, dict):
            continue

        for w in data.get("words", []):
            if isinstance(w, dict):
                eng = w.get("english", "").strip().lower()
                if eng:
                    words.add(eng)

    return words


# ===== FILTER SINGLE WORD MODE =====
def filter_single(words):
    if not ONLY_SINGLE_WORD:
        return words
    # single word = no spaces and no hyphens
    return {w for w in words if " " not in w and "-" not in w}


# ===== MAIN =====
def main():
    json_words = filter_single(load_json_words())
    audio_words = filter_single(load_audio_words())

    missing = sorted(json_words - audio_words)

    # WRITE RESULT
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        for w in missing:
            f.write(w + "\n")

    print(f"JSON words: {len(json_words)}")
    print(f"Audio words: {len(audio_words)}")
    print(f"Missing audio words written to 1-new-words.txt: {len(missing)}")


if __name__ == "__main__":
    main()
