from itertools import islice



def load_file():
    """ Load the content of a file. """
    with open("logs/auth.log", 'r') as f:
        file = f.readlines()
        
    return file
    
    # for lines in file[:5]:
    #     print("➡️", lines)
    
    

# def read_failed_logins(log_path, max_line=2):
    
#     """ Read the log file for unsuccessful login attempts. """
    
#     with open(log_path, 'r') as f:
#         for line in islice(f, max_line):
#             if "Failed Password" in line:
#                 failed_lines.append(line.strip())
#     return failed_lines