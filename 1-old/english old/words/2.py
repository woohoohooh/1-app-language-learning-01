import json

# имя файла
filename = "list_intermediate_1_common.json"   # поменяй на своё

with open(filename, "r", encoding="utf-8") as f:
    data = json.load(f)

# достаём английские слова
words_list = [item["english"] for item in data.get("words", [])]

print(words_list)
