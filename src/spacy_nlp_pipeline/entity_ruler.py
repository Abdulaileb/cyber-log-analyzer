import spacy



def loginFailedRecognizer():
    """ Create a custom pipeline component to recognize failed login attempts. """
    
    nlp = spacy.blank("en")
    pattern = [{"LOWER": "failed"}, {"LOWER": "password"}]
    ruler = nlp.add_pipe("entity_ruler", config={"overwrite_ents" : True})
    ruler.add_patterns([{"label": "FAILED_LOGIN", "pattern": pattern}])
    
    # doc = nlp(file)
    # failed_logins = [(ent.text, ent.label_) for ent in doc.ents if ent.label_ == "FAILED_LOGIN"]
    
    return nlp

def extraxt_data():
    "Create a rule to extract dates from the log entries."
    nlp = spacy.empty("en")
    ruler = nlp.add_pipe("entity_ruler", config={"overwrite_ents": True})
    ruler.add_patterns([{"label": "USER", "pattern": [{"LOWER": "user"}]}
                        , {"label": "IP_ADDRESS", "pattern": [{"LIKE_NUM": True}, {"TEXT": "."}, {"LIKE_NUM": True}, {"TEXT": "."}, {"LIKE_NUM": True}, {"TEXT": "."}, {"LIKE_NUM": True}]}
                        , {"label" : "SSH_KEY", "pattern": [{"LOWER": "ssh"}, {"LOWER": "key"}]},
                        {"label": "HOSTNAME", "pattern": [{"LOWER": "hostname"}]},
                        {"label": "DATE", "pattern": [{"SHAPE": "dd"}, {"TEXT": "/"}, {"SHAPE": "dd"}, {"TEXT": "/"}, {"SHAPE": "dddd"}]},
                        {"label": "TIME", "pattern": [{"SHAPE": "dd"}, {"TEXT": ":"}, {"SHAPE": "dd"}, {"TEXT": ":"}, {"SHAPE": "dd"}]},
                        {"label": "MESSAGE", "pattern": [{"LOWER": "message"}]},
                        {"label": "LOGIN", "pattern": [{"LOWER": "login"}]},
                        {"label": "FAILED_LOGIN", "pattern": [{"LOWER": "failed"}, {"LOWER": "login"}]}])
    return nlp

def ner():
    "Extract date from the log file."
    nlp = spacy.load("en_core_web_sm")
    return nlp


### regEx for date extraction


    
    
    