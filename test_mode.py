import spacy
from pathlib import Path
import json

# nlp = spacy.load("src/trainer/output/model-best")

# text = "Apr 29 07:21:01 example-server CRON[42069]: pam_unix(cron:session): session opened for user root by (uid=0)"
# doc = nlp(text)

# for ent in doc.ents:
#     print(ent.text, ent.label_)
    
    
data_dir = Path(__file__).resolve().parent


for file in data_dir.rglob('output.json'):
    print(f"Found: {file}")
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
def extract_failed_logins():
    result = data
    message_extract = [entry['Message'] for entry in result]
    return list(filter(lambda line: 'Failed password' in line, message_extract))

failed = extract_failed_logins()
for msg in failed:
    print(msg)
    
    
### Higer order functions refactor :

def extract_messages(filter_func):
    return list(filter(filter_func, [entry['Message'] for entry in data]))

#Closure factory
def make_keyword_filter(keyword):
    def filter_func(message):
        return keyword.lower() in message.lower()
    return filter_func


#Closure + Higher Orde Function:

failed_filter = make_keyword_filter("Failed password")
cron_filter = make_keyword_filter("cron")