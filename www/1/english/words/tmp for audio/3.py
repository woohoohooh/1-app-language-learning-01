import json
import os

def process_json_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "items" in data and isinstance(data["items"], list):
            for item in data["items"]:
                if isinstance(item, dict):
                    item.pop("id", None)
                    item.pop("audio", None)

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"Processed: {file_path}")

    except Exception as e:
        print(f"Error in {file_path}: {e}")


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    for filename in os.listdir(current_dir):
        if filename.lower().endswith(".json"):
            file_path = os.path.join(current_dir, filename)
            process_json_file(file_path)

    print("Done.")


if __name__ == "__main__":
    main()
