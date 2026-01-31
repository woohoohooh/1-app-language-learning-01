from PIL import Image
import os


def generate_icons():
    # Создайте основную иконку 512x512 и назовите ее icon.png
    # Затем запустите этот скрипт

    if not os.path.exists('icon.png'):
        print("Создайте иконку 512x512 и назовите ее icon.png")
        return

    sizes = [16, 48, 128]

    with Image.open('icon.png') as img:
        for size in sizes:
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            resized.save(f'icon-{size}x{size}.png')
            print(f'Создана иконка {size}x{size}')

    print("✅ Все иконки созданы!")


if __name__ == "__main__":
    generate_icons()