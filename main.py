from src.parser import *
from src.spacy_nlp_pipeline.entity_ruler import *
from src.analyzer import clean_log_line
import os
import re
import json 


##Refactor code:



def process_entity(ent, row, row_entities):
    
    if ent.label_ == "DATE":
        row["Date"] = ent.text
    elif ent.label_ == "TIME":
        row["Time"] = ent.text
    elif ent.label_ == "USER":
        if ent.text.lower().startswith("for "):
            row["User"] = ent.text.split(" ", 1)[1]
        elif ent.text.lower().startswith("user="):
            row["User"] = ent.text.split("=", 1)[1]
        else:
            row["User"] = ent.text
        row_entities.append(ent.text)
    elif ent.label_ == "IP_ADDRESS":
        if ent.text.lower().startswith("rhost="):
            row["IP Address"] = ent.text.split("=", 1)[1]
        else:
            row["IP Address"] = ent.text
        row_entities.append(ent.text)
    elif ent.label_ == "HOSTNAME":
        row["Hostname"] = ent.text
    elif ent.label_ == "SSH_KEY":
        row["Ssh_Key"] = ent.text
    elif ent.label_ == "PORT":
        tokens = ent.text.split()
        if len(tokens) == 2 and tokens[0].lower() == "port":
            row["Port"] = tokens[1]
        else:
            row["Port"] = ent.text.strip() or "None"
            
            
def process_log_lines(log_lines, nlp):
    rows = []
    for idx, line in enumerate(log_lines, 1):
        doc = nlp(line)
        row = {
            "ID": idx,
            "Date": "",
            "Time": "",
            "Message": "",
            "User": "",
            "IP Address": "",
            "Hostname": "",
            "Ssh_Key": "",
            "Port": ""
        }
        row_entities = []
        for ent in doc.ents:
            process_entity(ent, row, row_entities)
        raw_message = message_extraction(line)
        row["Message"] = clean_message(raw_message, row_entities)
        if any(row.values()):
            rows.append(row)
    return rows


def save_output(rows, output_log, headers):
    file_exists = os.path.exists(output_log)
    with open(output_log, "w") as f:
        json.dump(rows, f, indent=2)
    print(f"{'Overwritten' if file_exists else 'Extracted'} data saved to {output_log}")
    print(tabulate(rows, headers="keys", tablefmt="grid"))

if __name__ == "__main__":
    log_lines = load_file(max_length=20, preview=False)
    nlp = extract_data()
    headers = ["Date", "Time", "Message", "User", "IP Address", "Hostname", "Ssh_Key", "Port"]
    output_log = "logs/output.json"
    rows = process_log_lines(log_lines, nlp)
    save_output(rows, output_log, headers)