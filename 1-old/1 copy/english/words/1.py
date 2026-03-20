import os

for filename in os.listdir("."):
    if filename.endswith("_words.json"):
        new_name = filename.replace("_words.json", ".json")
        os.rename(filename, new_name)
        print(f"{filename} -> {new_name}")
