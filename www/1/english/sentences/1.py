import os

for filename in os.listdir("."):
    if filename.endswith("_sentences.json"):
        new_name = filename.replace("_sentences.json", ".json")
        os.rename(filename, new_name)
        print(f"{filename} -> {new_name}")
