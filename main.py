from src.parser import *
from src.spacy_nlp_pipeline.entity_ruler import *
import os
import re

if __name__ == "__main__":
    log_line = load_file()
    nlp = loginFailedRecognizer()
    
    for line in log_line[:10]:
        doc = nlp(line)
        for ent in doc.ents:
            if ent.label_ == "FAILED_LOGIN":
                print(f"Failed login detected: {ent.text} at line {ent.label_}")
                
                

# display_table = display_extracted_data()
# extract_date = entract_date()
# lo = load_file()  \d{2}:\d{2}:\d{2}

# for line in lo:
#     doc = extract_date(line)
#     for ent in doc.ents:
#         print(ent.text, ent.label_)

# nlp = extract_data()

# log_lines = open("logs/auth.log").readlines()

log_lines = load_file(max_length=10, preview=False)

nlp = extract_data()
rows = []

for line in log_lines:
    doc = nlp(line)
    print([(ent.text, ent.label_) for ent in doc.ents])  # Debugging output to see recognized entities
    
    row = {
        "Date": "",
        "Time": "",
        "Message": "",
        "User": "",
        "IP Address": "",
        "Hostname": "",
        "Ssh_Key": ""
    }
    for ent in doc.ents:
        if ent.label_ == "DATE":
            row["Date"] = ent.text
        elif ent.label_ == "TIME":
            row["Time"] = ent.text
        elif ent.label_ == "USER":
            tokens = ent.text.split()
            row["User"] = tokens[1] if len(tokens) > 1 else ent.text
        elif ent.label_ == "IP_ADDRESS":
            row["IP Address"] = ent.text
        elif ent.label_ == "MESSAGE":
            row["Message"] = ent.text
        elif ent.label_ == "HOSTNAME":
            row["Hostname"] = ent.text
        elif ent.label_ == "SSH_KEY":
            row["Ssh_Key"] = ent.text
            
    if any(row.values()):  # Skip empty rows
        rows.append(row)
        
# Print the result
headers = ["Date", "Time", "Message", "User", "IP Address", "Hostname", "Ssh_Key"]
print(tabulate(rows, headers="keys", tablefmt="grid"))
       
