from itertools import islice
from tabulate import tabulate 
import re



def load_file(max_length=10, preview=True):
    """ Load the content of a file. """
    with open("logs/auth.log", 'r') as f:
        file = f.readlines()
            
        # to avoid printed even whjen not needed, we need a flag
        if preview:
            for lines in file[:max_length]:
                print("➡️", lines.strip())
        
    return file[:max_length]


def display_extracted_data():
    """ Display the extracted data in a tabular format. """
    
    header = ["Date", "Time", "Message", "user", "IP Address", "Hostname", "Ssh_Key"]
    
    table = []
    data = load_file(5)
    
    for line in data:
        date_match = re.search(r"[A-Z][a-z]{2} \d{1,2}", line)
        time_match = re.search(r"\d{2}:\d{2}:\d{2}", line)
        user_match = re.search(r"for (?:invalid user )?(\w+)", line)
        message_match = re.search(r"]:(.*)", line)
        ip_address_match = re.search(r"\d{1,3}(?:\.\d{1,3}){3}", line)
        
        if date_match and time_match and message_match and ip_address_match:
            table.append([date_match.group(), time_match.group(), message_match.group(1).strip(), ip_address_match.group()])
    print(tabulate(table, headers=header, tablefmt="grid"))
    
    return table
            