import spacy
from spacy.pipeline import EntityRuler



def loginFailedRecognizer():
    """ Create a custom pipeline component to recognize failed login attempts. """
    
    nlp = spacy.blank("en")
    pattern = [{"LOWER": "failed"}, {"LOWER": "password"}]
    ruler = nlp.add_pipe("entity_ruler", config={"overwrite_ents" : True})
    ruler.add_patterns([{"label": "FAILED_LOGIN", "pattern": pattern}])
    
    # doc = nlp(file)
    # failed_logins = [(ent.text, ent.label_) for ent in doc.ents if ent.label_ == "FAILED_LOGIN"]
    
    return nlp

# def extraxt_data():
#     "Create a rule to extract dates from the log entries."
#     nlp = spacy.blank("en")
#     ruler = nlp.add_pipe("entity_ruler", config={"overwrite_ents": True})
#     ruler.add_patterns([{"label": "USER", "pattern": [{"LOWER": "for"}, {"IS_ALPHA": True}]},
                        
#                         #For the Ip address: match things like 192.168.0.3
                        
#                         {"label": "IP_ADDRESS", "pattern": [{"LIKE_NUM": True}, {"TEXT": "."}, {"LIKE_NUM": True}, {"TEXT": "."}, {"LIKE_NUM": True}, {"TEXT": "."}, {"LIKE_NUM": True}]},
#                         {"label" : "SSH_KEY", "pattern": [{"LOWER": "ssh"}, {"LOWER": "key"}]},
#                         {"label": "HOSTNAME", "pattern": [{"LOWER": "hostname"}, {"IS_ALPHA": True}]},
#                         {"label": "DATE", "pattern": [{"IS_TITLE": True}, {"IS_DIGIT": "True"}]},
#                         {"label": "TIME", "pattern": [{"IS_DIGIT": True}, {"TEXT": ":"}, {"IS_DIGIT": True}, {"TEXT": ":"}, {"IS_DIGIT": True}]},
#                         {"label": "MESSAGE", "pattern": [{"LOWER": "failed"}, {"LOWER": "password"}]} ])
#     return nlp


# def extract_data():
#     nlp = spacy.blank("en")
#     ruler = nlp.add_pipe("entity_ruler", config={"overwrite_ents": True})

#     patterns = [
#         # USER
#         {"label": "USER", "pattern": [{"LOWER": "for"}, {"IS_ALPHA": True}]},

#         # IP ADDRESS
#         {"label": "IP_ADDRESS", "pattern": [
#             {"LIKE_NUM": True}, {"TEXT": "."},
#             {"LIKE_NUM": True}, {"TEXT": "."},
#             {"LIKE_NUM": True}, {"TEXT": "."},
#             {"LIKE_NUM": True}
#         ]},

#         # DATE: Apr 29
#         {"label": "DATE", "pattern": [{"IS_TITLE": True}, {"IS_DIGIT": True}]},

#         # TIME: 06:56:50
#         {"label": "TIME", "pattern": [
#             {"IS_DIGIT": True}, {"TEXT": ":"},
#             {"IS_DIGIT": True}, {"TEXT": ":"},
#             {"IS_DIGIT": True}
#         ]},

#         # MESSAGE
#         {"label": "MESSAGE", "pattern": [{"LOWER": "failed"}, {"LOWER": "password"}]},

#         # HOSTNAME: e.g. example-server
#         {"label": "HOSTNAME", "pattern": [{"IS_ALPHA": True}, {"TEXT": "-"}, {"IS_ALPHA": True}]}
#     ]

#     ruler.add_patterns(patterns)
#     return nlp


def extract_data():
    """ Create a rule to extract dates from the log entries. """
    nlp = spacy.blank("en")
    ruler = nlp.add_pipe("entity_ruler", config={"overwrite_ents": True})

    patterns = [
        # Date: Apr 29
        {"label": "DATE", "pattern": [{"IS_TITLE": True}, {"IS_DIGIT": True}]},
        # Time: 06:56:50
        {"label": "TIME", "pattern": [{"SHAPE": "dd:dd:dd"}]},
        # Hostname: server
        {"label": "HOSTNAME", "pattern": [{"IS_ALPHA": True}, {"TEXT": "-"}, {"IS_ALPHA": True}]},
        # Message: Failed password
        {"label": "MESSAGE", "pattern": [{"LOWER": "failed"}, {"LOWER": "password"}]},
        # User: for root
        {"label": "USER", "pattern": [{"LOWER": "for"}, {"IS_ALPHA": True}]},
        # IP Address: 192.168.1.10
        {"label": "IP_ADDRESS", "pattern": [
            {"LIKE_NUM": True}, {"TEXT": "."},
            {"LIKE_NUM": True}, {"TEXT": "."},
            {"LIKE_NUM": True}, {"TEXT": "."},
            {"LIKE_NUM": True}
        ]},
        # SSH Key: optional, add if you have a pattern
    ]

    ruler.add_patterns(patterns)
    return nlp


def ner():
    "Extract date from the log file."
    nlp = spacy.load("en_core_web_sm")
    return nlp


### regEx for date extraction


    
    
    