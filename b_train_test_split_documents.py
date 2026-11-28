import os
import random
import shutil
from pathlib import Path

from program_params import (
    CATEGORIZATION_COUNTRIES,
    PREPROCESSED_COUNTRY_CORPUS_FOLDER,
    RANDOM_SEED,
    TEST_PREPROCESSED_COUNTRY_CORPUS_FOLDER,
    TRAIN_PREPROCESSED_COUNTRY_CORPUS_FOLDER,
    TRAIN_TEST_SPLIT,
)


def split_country_documents(
    country_code: str,
    preprocessed_country_dir: Path,
    train_country_dir: Path,
    test_country_dir: Path,
):
    print(f"Splitting documents for {country_code}")

    files = sorted(preprocessed_country_dir.glob("*.txt"))

    random.shuffle(files)
    train_split_index = int(len(files) * TRAIN_TEST_SPLIT)

    train_files = files[:train_split_index]
    test_files = files[train_split_index:]

    for file in train_files:
        shutil.copy2(file, train_country_dir / file.name)

    for file in test_files:
        shutil.copy2(file, test_country_dir / file.name)

    print(
        f"{country_code}: "
        f"{len(train_files)} training documents, "
        f"{len(test_files)} testing documents"
    )


def split_documents() -> None:
    print("Splitting preprocessed documents...")

    random.seed(RANDOM_SEED)

    preprocessed_dir = Path(PREPROCESSED_COUNTRY_CORPUS_FOLDER)
    train_dir = Path(TRAIN_PREPROCESSED_COUNTRY_CORPUS_FOLDER)
    test_dir = Path(TEST_PREPROCESSED_COUNTRY_CORPUS_FOLDER)

    for country_code in CATEGORIZATION_COUNTRIES:
        preprocessed_country_dir = preprocessed_dir / country_code

        if not preprocessed_country_dir.exists():
            print(f"Skipping {country_code}, directory not found")
            continue

        train_country_dir = train_dir / country_code
        test_country_dir = test_dir / country_code

        os.makedirs(train_country_dir, exist_ok=True)
        os.makedirs(test_country_dir, exist_ok=True)

        split_country_documents(
            country_code,
            preprocessed_country_dir,
            train_country_dir,
            test_country_dir,
        )

    print("Finished splitting documents")


if __name__ == "__main__":
    split_documents()
