import os

# Работает в текущей папке
for filename in os.listdir(''):
    if filename.lower().endswith('.wav'):
        new_name = filename.replace('_', ' ')
        if new_name != filename:
            print(f'Rename: "{filename}" → "{new_name}"')
            os.rename(filename, new_name)
