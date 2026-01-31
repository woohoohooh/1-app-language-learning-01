import os
import json
from pathlib import Path


def find_missing_words():
    """
    Находит английские слова без аудиофайлов и сохраняет их в new.txt
    Возвращает список отсутствующих слов
    """

    # Получаем текущую директорию
    current_dir = Path(__file__).parent.absolute()
    print(f"Текущая директория: {current_dir}")

    # Определяем пути к папкам
    english_dir = current_dir / "english"
    audio_dir = current_dir / "audio"
    output_file = current_dir / "new.txt"

    # Проверяем существование папок
    if not english_dir.exists():
        print(f"ОШИБКА: Папка 'english' не найдена в {current_dir}")
        print("Создайте папку 'english' и поместите в нее JSON файлы")
        return []

    if not audio_dir.exists():
        print(f"ОШИБКА: Папка 'audio' не найдена в {current_dir}")
        print("Создайте папку 'audio' и поместите в нее WAV файлы")
        return []

    print(f"Папка с JSON файлами: {english_dir}")
    print(f"Папка с аудиофайлами: {audio_dir}")
    print(f"Выходной файл: {output_file}")

    # Собираем все .wav файлы из папки audio
    audio_files = set()
    wav_count = 0

    try:
        # Ищем все .wav файлы в папке audio
        for file_path in audio_dir.glob("*.wav"):
            # Берем имя файла без расширения и в нижнем регистре
            file_name = file_path.stem.lower()
            audio_files.add(file_name)
            wav_count += 1

        print(f"Найдено {wav_count} .wav файлов в папке audio")
        if wav_count < 10 and wav_count > 0:
            print("Примеры найденных файлов:", list(audio_files)[:5])
    except Exception as e:
        print(f"Ошибка при чтении папки audio: {e}")
        return []

    # Ищем JSON файлы
    json_files = list(english_dir.glob("*.json"))
    print(f"Найдено {len(json_files)} JSON файлов в папке english")

    if not json_files:
        print("Нет JSON файлов в папке english")
        return []

    # Множество для хранения слов без аудио
    missing_words = set()

    # Обрабатываем каждый JSON файл
    for json_file in json_files:
        print(f"Обработка файла: {json_file.name}")

        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Проверяем структуру файла
            if "words" not in data:
                print(f"  Предупреждение: в файле {json_file.name} нет ключа 'words'")
                continue

            words_count = len(data["words"])
            print(f"  Найдено {words_count} слов в файле")

            # Проверяем каждое слово
            for word_data in data["words"]:
                english_word = word_data.get("english", "").strip()
                if not english_word:
                    continue

                # Проверяем наличие аудиофайлов для этого слова
                audio_list = word_data.get("audio", [])
                has_audio = False

                for audio_path in audio_list:
                    if not audio_path:
                        continue

                    # Извлекаем имя файла из пути
                    # Путь может быть: "audio/word.wav" или просто "word.wav"
                    if "/" in audio_path:
                        audio_name = audio_path.split("/")[-1]
                    else:
                        audio_name = audio_path

                    # Убираем расширение .wav и приводим к нижнему регистру
                    if audio_name.lower().endswith('.wav'):
                        audio_name = audio_name[:-4].lower()
                    else:
                        audio_name = audio_name.lower()

                    # Проверяем, есть ли такой файл
                    if audio_name in audio_files:
                        has_audio = True
                        break

                # Если аудиофайла нет, добавляем слово в список
                if not has_audio:
                    missing_words.add(english_word)
                    print(f"  Нет аудио для слова: '{english_word}'")

        except json.JSONDecodeError as e:
            print(f"  Ошибка JSON в файле {json_file.name}: {e}")
        except Exception as e:
            print(f"  Ошибка при чтении файла {json_file.name}: {e}")

    # Сохраняем результат
    print(f"\nНайдено {len(missing_words)} слов без аудиофайлов")

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            if missing_words:
                # Сортируем слова по алфавиту
                for word in sorted(missing_words):
                    f.write(f"{word}\n")
                print(f"Список сохранен в файл: {output_file}")
                print(f"Файл успешно создан по пути: {output_file.absolute()}")

                # Показываем несколько слов из списка
                sample_words = list(sorted(missing_words))[:10]
                print(f"Первые слова из списка: {', '.join(sample_words)}")
                if len(missing_words) > 10:
                    print(f"... и еще {len(missing_words) - 10} слов")
            else:
                f.write("")  # Создаем пустой файл
                print("Все слова имеют аудиофайлы. Файл new.txt создан пустым.")

        # Проверяем, что файл действительно создан
        if output_file.exists():
            print(f"✓ Файл успешно создан: {output_file}")
            # Показываем размер файла
            file_size = output_file.stat().st_size
            print(f"Размер файла: {file_size} байт")
        else:
            print(f"✗ Ошибка: файл {output_file} не был создан")

    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")
        return []

    return sorted(missing_words)


# Альтернативная функция с подробным логированием в файл
def find_missing_words_with_log():
    """То же самое, но с дополнительным лог-файлом"""

    current_dir = Path(__file__).parent.absolute()
    log_file = current_dir / "script_log.txt"

    # Перенаправляем вывод в лог-файл и консоль
    import sys

    class Tee:
        def __init__(self, *files):
            self.files = files

        def write(self, obj):
            for f in self.files:
                f.write(obj)

        def flush(self):
            for f in self.files:
                if hasattr(f, 'flush'):
                    f.flush()

    # Открываем лог-файл
    with open(log_file, 'w', encoding='utf-8') as log_f:
        original_stdout = sys.stdout
        sys.stdout = Tee(sys.stdout, log_f)

        try:
            result = find_missing_words()
        finally:
            sys.stdout = original_stdout

    print(f"\nЛог выполнения сохранен в: {log_file}")
    return result


if __name__ == "__main__":
    print("=" * 60)
    print("ПОИСК СЛОВ БЕЗ АУДИОФАЙЛОВ")
    print("=" * 60)
    print("Скрипт ищет в папке 'english' JSON файлы,")
    print("проверяет наличие аудиофайлов в папке 'audio'")
    print("и сохраняет слова без аудио в файл 'new.txt'")
    print("=" * 60)

    # Запускаем основную функцию
    missing_words = find_missing_words()

    # Если файл не появился, показываем дополнительные инструкции
    output_file = Path(__file__).parent.absolute() / "new.txt"
    if not output_file.exists():
        print("\n" + "!" * 60)
        print("Файл new.txt не был создан. Возможные причины:")
        print("1. Проверьте права на запись в текущей директории")
        print("2. Убедитесь, что папки 'english' и 'audio' существуют")
        print("3. Проверьте структуру папок:")
        print(f"   Текущая директория: {Path(__file__).parent.absolute()}")
        print("   Должна содержать:")
        print("   - ваш_скрипт.py")
        print("   - папку 'english/' с JSON файлами")
        print("   - папку 'audio/' с WAV файлами")
        print("!" * 60)

        # Создаем тестовый файл для проверки прав
        try:
            test_file = Path(__file__).parent.absolute() / "test_write.txt"
            with open(test_file, 'w') as f:
                f.write("test")
            test_file.unlink()  # Удаляем тестовый файл
            print("✓ Права на запись в директорию есть")
        except Exception as e:
            print(f"✗ Ошибка записи в директорию: {e}")

    print("\n" + "=" * 60)
    print("СКРИПТ ЗАВЕРШЕН")
    print("=" * 60)