from src.parser import *
from src.spacy_nlp_pipeline.entity_ruler import *
from src.analyzer import clean_log_line
import os
import re
import json 

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

log_lines = load_file(max_length=20, preview=False)

nlp = extract_data()
rows = []
row_entities = []

for line in log_lines:
    doc = nlp(line)
    print([(ent.text, ent.label_) for ent in doc.ents])  
    
    row = {
        "ID": len(rows) + 1,
        "Date": "",
        "Time": "",
        "Message": "",
        "User": "",
        "IP Address": "",
        "Hostname": "",
        "Ssh_Key": "",
        "Port" : ""
    }
    for ent in doc.ents:
        if ent.label_ == "DATE":
            row["Date"] = ent.text
        elif ent.label_ == "TIME":
            row["Time"] = ent.text
        elif ent.label_ == "USER":
            #for root
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
                row["Port"] = ent.text
            
    #Use message extraction
    raw_message = message_extraction(line)
    row["Message"] = clean_message(raw_message, row_entities)
            
    if any(row.values()):  # Skip empty rows
        rows.append(row)
        
# Print the result
headers = ["Date", "Time", "Message", "User", "IP Address", "Hostname", "Ssh_Key", "Port"]

output_log = "logs/output.json"
file_path = os.path.exists(output_log)

#write rows as JSON (create or overwrite)
with open(output_log, "w") as f:
    json.dump(rows, f, indent=2)
    if file_path:
        print(f"File {output_log} already exists. Overwriting it.")
    else:
        print(f"Extracted data saved to {output_log}")

print(tabulate(rows, headers="keys", tablefmt="grid"))
       



#log the error:
# Add this to debug
# doc = nlp("Apr 29 06:57:19 example-server sshd[38780]: Connection closed by 123.183.209.132 [preauth]")
# for token in doc:
#     print(repr(token.text), token.pos_, token.is_alpha, token.is_digit)
    
    
# print("Extracted entities:")
# #Clean Data
# log_lines = open("logs/auth_copy.log").readlines()

# cleaned_data = "logs/cleaned_data.txt"

# with open(cleaned_data, "w") as f:
#     for line in log_lines:
#         cleaned_line, kv_dict = clean_log_line(line)
#         f.write(f"cleaned line: {cleaned_line},\n", )
#         print("Cleaned:", cleaned_line)
#         print("Extracted fields:", kv_dict)