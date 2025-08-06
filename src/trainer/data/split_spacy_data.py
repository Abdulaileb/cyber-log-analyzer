# import random
# from pathlib import Path
# from spacy.tokens import DocBin
# import spacy


# def load_docs(data_path: Path, lang: str = "en") -> list:
    
#     """
#     Load spaCy Doc objects from a .spacy file.

#     Args:
#         data_path (Path): Path to the .spacy file.
#         lang (str): Language model to use (default: 'en').

#     Returns:
#         List of Doc objects.
#     """
    
#     nlp = spacy.blank(lang)
#     doc_bin = DocBin().from_disk(data_path)
#     return list(doc_bin.get_docs(nlp.vocab))


# full_data_path = "train.spacy"
# nlp = spacy.blank("en")


# ### Now we split the doc container
# def split_docs(docs: list, train_ratio: float = 0.8, seed: int = 42) -> tuple:
    
#     """
#         Shuffle and split documents into train and dev sets.

#         Args:
#             docs (list): List of Doc objects.
#             train_ratio (float): Proportion of data for training (default: 0.8).
#             seed (int): Random seed for reproducibility.

#         Returns:
#             Tuple: (train_docs, dev_docs)
#     """
    
#     assert 0 < train_ratio < 1, "Train_ratio must be between 0 and 1"
    
#     if seed is not None:
#         random.seed(seed)
        
#     shuffled_docs = docs.copy()
#     random.shuffle(shuffled_docs)
    
#     split_idx = int(train_ratio * len(shuffled_docs))
#     return shuffled_docs[:split_idx], shuffled_docs[split_idx:]


# def save_docs(docs: list, output_path: Path) -> None:
#     """
#     Save a list of Doc objects to a .spacy file.

#     Args:
#         docs (list): List of Doc objects.
#         output_path (Path): Output file path.
#     """
#     doc_bin = DocBin(docs=docs)
#     doc_bin.to_disk(output_path)
#     print(f"Saved {len(docs)} docs to {output_path}")


# data_splitter.py

import random
from pathlib import Path
from spacy.tokens import DocBin
import spacy


def load_spacy_docs(file_path: str, lang: str = "en"):
    """
    Load docs from a .spacy file.
    """
    nlp = spacy.blank(lang)
    doc_bin = DocBin().from_disk(file_path)
    return list(doc_bin.get_docs(nlp.vocab))


def split_docs(docs, train_ratio=0.8):
    """
    Shuffle and split docs into train and dev.
    Returns (train_docs, dev_docs).
    """
    shuffled_docs = docs.copy()
    random.shuffle(shuffled_docs)
    split_idx = int(len(shuffled_docs) * train_ratio)
    return shuffled_docs[:split_idx], shuffled_docs[split_idx:]


def save_docs(docs, file_path: str):
    """
    Save docs to a .spacy file.
    """
    DocBin(docs=docs).to_disk(file_path)


# --- Main Execution (only runs when this file is executed directly) ---

if __name__ == "__main__":
    # Paths and settings
    input_path = "train.spacy"
    train_output = "train_split.spacy"
    dev_output = "dev_split.spacy"

    # Load, split, save
    docs = load_spacy_docs(input_path)
    train_docs, dev_docs = split_docs(docs, train_ratio=0.8)
    save_docs(train_docs, train_output)
    save_docs(dev_docs, dev_output)

    print(f"Split {len(docs)} docs: {len(train_docs)} for training, {len(dev_docs)} for dev.")