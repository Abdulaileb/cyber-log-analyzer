import spacy
from spacy.pipeline import EntityRuler  


def make_pipeline():
    "This is a fnx to make pipllines"
    nlp = spacy.blank("en")
    ruler = nlp.add_pipe("entity_ruler", config={"overwrite_ents": True})
    ruler.add_patterns([...])
    return nlp


def load_data():
    nlp = spacy.load("en")
    return nlp