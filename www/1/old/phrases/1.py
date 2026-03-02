import os

for filename in os.listdir("."):
    if filename.endswith("_phrases.json"):
        new_name = filename.replace("_phrases.json", ".json")
        os.rename(filename, new_name)
        print(f"{filename} -> {new_name}")
