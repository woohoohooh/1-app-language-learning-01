import os
import json
from urllib.parse import unquote

# Папки
json_folder = r'C:\1py\html\english'
audio_folder = r'C:\1py\html\audio'

# Все файлы WAV в папке audio (в lower case)
audio_files = set(f.lower() for f in os.listdir(audio_folder))

# Перебор JSON
json_files = [f for f in os.listdir(json_folder) if f.lower().endswith('.json')]

# Множество для уникальных слов
missing_words = set()

for jfile in json_files:
    jpath = os.path.join(json_folder, jfile)
    with open(jpath, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f'{jfile} - invalid JSON, skipped')
            continue

    # Проверяем, что JSON словарь с ключом 'words'
    if isinstance(data, dict) and 'words' in data:
        words = data['words']
    else:
        continue

    for w in words:
        english_word = w.get('english')
        if not english_word:
            continue

        # Проверяем, есть ли хоть один файл из audio для этого слова
        found = False
        for audio_path in w.get('audio', []):
            audio_name = os.path.basename(unquote(audio_path)).lower()
            if audio_name in audio_files:
                found = True
                break

        if not found:
            missing_words.add(english_word.lower())  # записываем слово в lower case

# Записываем результат в new.txt
with open('new.txt', 'w', encoding='utf-8') as f:
    for word in sorted(missing_words):
        f.write(word + '\n')

print(f'Finished! {len(missing_words)} missing words written to new.txt')
