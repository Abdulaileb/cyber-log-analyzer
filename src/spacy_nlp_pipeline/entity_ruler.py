import spacy
from spacy.pipeline import EntityRuler
from spacy.matcher import Matcher 
from spacy.language import Language
import re




def loginFailedRecognizer():
    """ Create a custom pipeline component to recognize failed login attempts. """
    
    nlp = spacy.blank("en")
    pattern = [{"LOWER": "failed"}, {"LOWER": "password"}]
    ruler = nlp.add_pipe("entity_ruler", config={"overwrite_ents" : True})
    ruler.add_patterns([{"label": "FAILED_LOGIN", "pattern": pattern}])
     
    return nlp

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
        {"label": "USER", "pattern": [{"LOWER": "for"}, {"IS_ALPHA": True},]},
        {"label": "USER", "pattern": [{"LOWER": "user"}, {"TEXT": "="}, {"IS_ALPHA": True}]},
        # Port: 38399 -- > "Lower" try to make it more specific to find others
        {"label": "PORT", "pattern": [
            {"LOWER": "port"}, {"IS_DIGIT": True}
        ]},
    ]

    ruler.add_patterns(patterns)
    
    matcher = Matcher(nlp.vocab)
    matcher.add("SSH_KEY", [[
        {"TEXT" : {"REGEX" : r"^[a-zA-Z]+[\[].*"}},
        {"TEXT": "]"},
        {"TEXT": ":"}
    ]])
    
    matcher.add("IP_ADDRESS", [
        [{"TEXT": {"REGEX": r"^\d{1,3}(\.\d{1,3}){3}$"}}],
        [{"TEXT" : {"REGEX" : r"^[a-zA-z]+=\d{1,3}(\.\d{1,3}){3}:\d{1,5}$"}}],
        [{"TEXT": {"REGEX": r"^[a-zA-Z]+=\d{1,3}(\.\d{1,3}){3}$"}}]
    ])

    
    # Custom component to match SSH keys
    
    @Language.component("ssh_key_component")
    def custom_component(doc):
        spans = list(doc.ents)
        matches = matcher(doc)
        for match_id, start, end in matches:
            label = nlp.vocab.strings[match_id]
            span = spacy.tokens.Span(doc, start, end, label=label)
            spans.append(span)
            # span = doc[start:end]
        filtered = spacy.util.filter_spans(spans)
        doc.ents = filtered
        return doc
    
    nlp.add_pipe("ssh_key_component", after="entity_ruler")
    
    return nlp



def ner():
    "Extract date from the log file."
    nlp = spacy.load("en_core_web_sm")
    return nlp



# the message function
def message_extraction(line):
    # Find the first colon followed by a space (": ")
    match = re.search(r":\s", line)
    if match:
        # Extract everything after that colon+space
        return line[match.end():].strip()
    return line.strip()

def clean_message(message, entities):
    # entities: list of entity texts to remove from message
    for ent in entities:
        # Remove the entity text from the message
        message = message.replace(ent, "")
    # Remove extra spaces left after removal
    message = re.sub(r'\s+', ' ', message).strip()
    return message


    
    
    