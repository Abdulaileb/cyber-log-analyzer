import random
from spacy.tokens import DocBin
import spacy



full_data_path = "train.spacy"
nlp = spacy.blank("en")
doc_bin = DocBin().from_disk(full_data_path)
docs = list(doc_bin.get_docs(nlp.vocab))

# Shuffle and split (80% train, 20% dev)
random.shuffle(docs)
split = int(0.8 * len(docs))
train_docs = docs[:split]
dev_docs = docs[split:]

# Save them
DocBin(docs=train_docs).to_disk("train_split.spacy")
DocBin(docs=dev_docs).to_disk("dev_split.spacy")

print(f"Split {len(docs)} docs: {len(train_docs)} for training, {len(dev_docs)} for dev.")
