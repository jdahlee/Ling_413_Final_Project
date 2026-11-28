import os
import random
from pathlib import Path

from program_params import (
    CATEGORIZATION_COUNTRIES,
    COUNTRY_CORPUS_FOLDER,
    COUNTRY_DOCUMENT_CAP,
    COUNTRY_DOCUMENT_NO_CAP_FLAG,
    PREPROCESS_CHARACTERS_TO_REMOVE,
    PREPROCESSED_COUNTRY_CORPUS_FOLDER,
    RANDOM_SEED,
)


def preprocess_document(document: str) -> str:
    document = document.strip().lower()

    for character in PREPROCESS_CHARACTERS_TO_REMOVE:
        document = document.replace(character, "")

    return document


def preprocess_country_documents(
    country_code: str, country_dir: Path, preprocessed_country_dir: Path
):
    print(f"Beginning to process {country_code}")

    files = sorted(country_dir.glob("*.txt"))
    if COUNTRY_DOCUMENT_CAP != COUNTRY_DOCUMENT_NO_CAP_FLAG:
        print(
            f"COUNTRY_DOCUMENT_CAP set to {COUNTRY_DOCUMENT_CAP}, randomly selecting {COUNTRY_DOCUMENT_CAP} files with seed {RANDOM_SEED}"
        )
        random.seed(RANDOM_SEED)
        random.shuffle(files)
        files = files[:COUNTRY_DOCUMENT_CAP]

    for documents_processed, file in enumerate(files):
        text = file.read_text(encoding="utf-8", errors="ignore")
        preprocessed_doc = preprocess_document(text)
        preprocessed_doc_name = "preprocessed_" + file.name
        preprocessed_doc_path = Path(preprocessed_country_dir, preprocessed_doc_name)

        with open(preprocessed_doc_path, mode="w") as file:
            file.write(preprocessed_doc)

        if (documents_processed + 1) % 100 == 0:
            print(
                f"Processed {documents_processed + 1} documents for country {country_code}"
            )

    print(
        f"Finished preprocessing {country_code} documents, data output to {preprocessed_country_dir}"
    )


def preprocess_documents() -> None:
    print("Preprocessing documents...")

    corpus_dir = Path(COUNTRY_CORPUS_FOLDER)
    for country_dir in corpus_dir.iterdir():
        if not country_dir.is_dir():
            continue

        country_code = country_dir.name
        if country_code not in CATEGORIZATION_COUNTRIES:
            continue

        preprocessed_country_dir = Path(
            PREPROCESSED_COUNTRY_CORPUS_FOLDER, country_code
        )
        if preprocessed_country_dir.exists():
            print(f"Skipping {country_code}, already processed")
            continue

        os.makedirs(preprocessed_country_dir, exist_ok=True)
        preprocess_country_documents(
            country_code, country_dir, preprocessed_country_dir
        )

    print("Finished preprocessing documents")


if __name__ == "__main__":
    preprocess_documents()
