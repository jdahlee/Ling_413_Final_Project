import os
from collections import defaultdict
from pathlib import Path

import nltk
import pandas as pd
from nltk.corpus import stopwords

from program_params import (
    COUNTRY_CODE_COLUMN_TITLE,
    TEST_COUNTRY_WORD_FREQUENCY_DATA_FOLDER,
    TEST_PREPROCESSED_COUNTRY_CORPUS_FOLDER,
    TRAIN_COUNTRY_WORD_FREQUENCY_DATA_FOLDER,
    TRAIN_PREPROCESSED_COUNTRY_CORPUS_FOLDER,
)


def find_word_counts(doc_text: str):
    doc_words = doc_text.split()

    stop_words = set(stopwords.words("english"))
    doc_words = [word for word in doc_words if word not in stop_words]

    freq_dict = defaultdict(int)
    for word in doc_words:
        freq_dict[word] += 1

    return freq_dict


def process_country(country_code: str, country_dir: Path, out_file_path: Path):
    print(f"Beginning to process {country_code}")

    rows = []
    doc_ids = []

    files = sorted(country_dir.glob("*.txt"))
    for documents_processed, file in enumerate(files):
        text = file.read_text(encoding="utf-8", errors="ignore")
        rows.append(find_word_counts(text))
        doc_ids.append(f"{country_code}_{file.stem}")

        if (documents_processed + 1) % 100 == 0:
            print(
                f"Processed {documents_processed + 1} documents for country {country_code}"
            )

    df = pd.DataFrame(rows, index=doc_ids)
    df = df.fillna(0).astype(int)
    df[COUNTRY_CODE_COLUMN_TITLE] = country_code
    print("Exporting data frame..")
    df.to_parquet(
        out_file_path
    )  # export as parquet file becuase of how sparse + large the dfs are
    print(
        f"Finished processing {country_code} documents, word frequency data output to {out_file_path}"
    )


def collect_word_frequencies():
    # Make directory to output frequency data files
    print("Collecting country word frequencies...")

    print(
        f"Outputing training country word frequecy data to: {TRAIN_COUNTRY_WORD_FREQUENCY_DATA_FOLDER}"
    )
    os.makedirs(TRAIN_COUNTRY_WORD_FREQUENCY_DATA_FOLDER, exist_ok=True)
    print(
        f"Outputing testing country word frequecy data to: {TEST_COUNTRY_WORD_FREQUENCY_DATA_FOLDER}"
    )
    os.makedirs(TEST_COUNTRY_WORD_FREQUENCY_DATA_FOLDER, exist_ok=True)

    nltk.download("stopwords")
    nltk.download("punkt")

    train_corpus_dir = Path(TRAIN_PREPROCESSED_COUNTRY_CORPUS_FOLDER)
    test_corpus_dir = Path(TEST_PREPROCESSED_COUNTRY_CORPUS_FOLDER)
    corpus_dirs = [
        ("train", train_corpus_dir, TRAIN_COUNTRY_WORD_FREQUENCY_DATA_FOLDER),
        ("test", test_corpus_dir, TEST_COUNTRY_WORD_FREQUENCY_DATA_FOLDER),
    ]

    for label, corpus_dir, frequency_data_dir in corpus_dirs:
        print(f"Collecting {label} country word frequencies")
        for country_dir in corpus_dir.iterdir():
            if not country_dir.is_dir():
                continue
            country_code = country_dir.name

            out_file_name = f"{label}_{country_code}_word_counts.parquet"
            out_file_path = Path(frequency_data_dir, out_file_name)
            if out_file_path.exists():
                print(f"Skipping {country_code}, already processed")
                continue

            process_country(country_code, country_dir, out_file_path)

        print(f"Finished collecting {label} country word frequencies\n")


if __name__ == "__main__":
    collect_word_frequencies()
