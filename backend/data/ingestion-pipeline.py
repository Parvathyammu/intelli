from dotenv import load_dotenv
import os
import json
from triplet_extractor import extract_triplets
from triplet_ingestion import insert_triplets

load_dotenv()

DATA_FOLDER = "mosdac_scraped"


def process_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        text = data["text"]

        triplets = extract_triplets(text)

        if not triplets:
            print("❌ No triplets:", filepath)
            return False

        insert_triplets(triplets)

        print("✅ Processed:", filepath)
        return True

    except Exception as e:
        print("❌ Error:", e)
        return False


def main():
    passed = 0
    total = 0

    for file in os.listdir(DATA_FOLDER):
        path = os.path.join(DATA_FOLDER, file)

        if os.path.isfile(path):
            total += 1

            if process_file(path):
                passed += 1

    print(f"\nPassed {passed}/{total}")


if __name__ == "__main__":
    main()