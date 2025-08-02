# import json
# import spacy
# from spacy.tokens import DocBin
# from pathlib import Path


# #Load the model for me
# nlp = spacy.blank("en")
# doc_bin = DocBin()
# data = None

# #load the json file

# base_dir = Path(__file__).resolve().parents[2]

# for file in base_dir.rglob('export_177092_project-177092-at-2025-08-01-23-49-ac8aa10b.json'):
#     print(f"Found: {file}")
    
#     with open(file, "r", encoding="utf-8") as f:
#         data = json.load(f)
        
        
# #since the json structure is different, we have to find a way to loop through it

# for item in data:
#     text = item["data"]["text"]
#     spans = []
#     annotations = item.get("annotations", [])
    
#     if not annotations:
#         continue
    
#     for result in annotations[0]["result"]:
#         start = result["value"]["start"]
#         end = result["value"]["end"]
#         label = result["value"]["labels"][0]
        
#         span = (start, end, label)
#         spans.append(span)
        
#     doc = nlp.make_doc(text)
#     ents = []
#     for start, end, label in spans:
#         span = doc.char_span(start, end, label=label)
#         if span is None:
#             print(f"Skipping entity: {text[start:end]} ({label})")
#         else:
#             ents.append(span)
            
#     doc.ents = ents
#     doc_bin.add(doc)
    
# #Save the format as SpaCy

# output_path = Path("data/train.spacy")
# output_path.parent.mkdir(parents=True, exist_ok=True)
# doc_bin.to_disk(output_path)
        
### I had an issues with irregularities of the data 
## Some data has "root", whilst others may get "root "... these are all irregularities that spacy doesn't accept 





import json
import spacy
from spacy.tokens import DocBin
from pathlib import Path

# Load blank English pipeline
nlp = spacy.blank("en")
doc_bin = DocBin()
base_dir = Path(__file__).resolve().parents[2]

def make_best_span(doc, start, end, label):
    
    """Try to get a valid span with fallback strategies."""
    # direct
    span = doc.char_span(start, end, label=label, alignment_mode="strict")
    if span:
        return span
    # expand to nearest token boundaries
    span = doc.char_span(start, end, label=label, alignment_mode="expand")
    if span:
        return span
    
    # contract to fit inside token boundaries
    span = doc.char_span(start, end, label=label, alignment_mode="contract")
    
    if span:
        return span
    # try trimming whitespace from original text slice and adjust
    text_slice = doc.text[start:end]
    trimmed = text_slice.strip()
    if not trimmed:
        return None
    
    # find trimmed within original and attempt again
    new_start = doc.text.find(trimmed, start, end)
    if new_start != -1:
        new_end = new_start + len(trimmed)
        span = doc.char_span(new_start, new_end, label=label, alignment_mode="expand")
        if span:
            return span
    return None

for file in base_dir.rglob('export_177092_project-177092-at-2025-08-01-23-49-ac8aa10b.json'):
    print(f"Found: {file}")
    
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

for item in data:
    text = item["data"].get("text", "")
    if not text:
        continue
    annotations = item.get("annotations", [])
    if not annotations:
        continue  # skip if nothing annotated

    doc = nlp.make_doc(text)
    candidate_spans = []

    # Extract all annotated spans (we assume single annotation per item as typical)
    for result in annotations[0].get("result", []):
        start = result["value"]["start"]
        end = result["value"]["end"]
        labels = result["value"].get("labels", [])
        if not labels:
            continue
        label = labels[0]
        span = make_best_span(doc, start, end, label)
        if span is None:
            original = text[start:end]
            print(f"⚠️  Could not align span: '{original}' ({label}) in: {text}")
        else:
            candidate_spans.append(span)

    # Filter overlapping spans: prefer longer spans first
    candidate_spans.sort(key=lambda s: (s.end - s.start), reverse=True)
    selected = []
    occupied_token_idxs = set()

    for span in candidate_spans:
        overlap = False
        for tok in span:
            if tok.i in occupied_token_idxs:
                overlap = True
                break
        if not overlap:
            selected.append(span)
            for tok in span:
                occupied_token_idxs.add(tok.i)
        else:
            # Overlapping span skipped
            print(f"ℹ️  Skipped overlapping span: '{span.text}' ({span.label_})")

    doc.ents = selected
    doc_bin.add(doc)

doc_bin.to_disk("train.spacy")
print("✅ Saved train.spacy with", len(list(doc_bin.get_docs(nlp.vocab))), "docs")
