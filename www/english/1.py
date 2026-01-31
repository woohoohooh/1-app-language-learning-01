import os
import json

for filename in os.listdir(''):
    if filename.lower().endswith('.json'):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        def replace_in_obj(obj):
            if isinstance(obj, dict):
                return {k: replace_in_obj(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [replace_in_obj(x) for x in obj]
            elif isinstance(obj, str):
                return obj.replace('_', '%20')
            else:
                return obj

        new_data = replace_in_obj(data)

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=2)

        print(f'Updated {filename}')
