# Random Seed
RANDOM_SEED = 1

COUNTRY_DOCUMENT_NO_CAP_FLAG = -1
COUNTRY_DOCUMENT_CAP = 2500
COUNTRY_CORPUS_FOLDER = "Country_Corpus"
PREPROCESS_CHARACTERS_TO_REMOVE = []

PREPROCESSED_COUNTRY_CORPUS_FOLDER = "Preprocessed_Country_Corpus"
CATEGORIZATION_COUNTRIES = ["gb", "hk", "in", "lk", "ng", "ph", "tz", "us"]

TRAIN_PREPROCESSED_COUNTRY_CORPUS_FOLDER = "Train_Preprocessed_Country_Corpus"
TEST_PREPROCESSED_COUNTRY_CORPUS_FOLDER = "Test_Preprocessed_Country_Corpus"
TRAIN_TEST_SPLIT = 0.9

COUNTRY_CODE_COLUMN_TITLE = "Country Code"
TRAIN_COUNTRY_WORD_FREQUENCY_DATA_FOLDER = "Train_Country_Word_Frequency_Data"
TEST_COUNTRY_WORD_FREQUENCY_DATA_FOLDER = "Test_Country_Word_Frequency_Data"
MIN_DOC_FREQ = 5  # How many docs within a country's corpus a word must appear in for us to not prune it
