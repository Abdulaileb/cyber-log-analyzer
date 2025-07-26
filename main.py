from src.parser import load_file
from src.spacy_nlp_pipeline.entity_ruler import *
import os

if __name__ == "__main__":
    log_line = load_file()
    nlp = loginFailedRecognizer()
    
    for line in log_line[:10]:
        doc = nlp(line)
        for ent in doc.ents:
            if ent.label_ == "FAILED_LOGIN":
                print(f"Failed login detected: {ent.text} at line {ent.label_}")
                

extract_date = entract_date()
lo = load_file()

for line in lo:
    doc = extract_date(line)
    for ent in doc.ents:
        print(ent.text, ent.label_)

