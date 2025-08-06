import re

#Clean the log line by removing extra spaces and splitting key-value pairs

def clean_log_line(line):
    """ Clean the log line by removing extra spaces and splitting key-value pairs. """
    # Remove extra spaces
    line = line.strip()
    # Replace multiple spaces/tabs with a single space
    line = re.sub(r'\s+', ' ', line)
    # Split key-value pairs into a dictionary
    kv_pattern = re.findall(r'(\w+)=([^\s]+)', line)
    kv_dict = {k: v for k, v in kv_pattern}
    return line, kv_dict