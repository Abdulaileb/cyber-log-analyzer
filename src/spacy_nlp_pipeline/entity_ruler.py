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

def entract_date():
    "Extract date from the log file."
    nlp = spacy.load("en_core_web_sm")
    return nlp

    
    
    