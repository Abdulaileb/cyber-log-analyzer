# ner_app.py

import streamlit as st
import spacy
from spacy import displacy

st.set_page_config(page_title="Cybersecurity NER", layout="wide")

# Load your trained model
@st.cache_resource
def load_model():
    return spacy.load("src/trainer/output/model-best")  # adjust path if needed

nlp = load_model()

st.title(" Cybersecurity Log Entity Recognition")
st.markdown("Enter a log message and see named entities like **IP_ADDRESS, TOOL, USERNAME, PORT** highlighted!")

# Text input
text_input = st.text_area("Enter Log Text", height=150, placeholder="Paste log message here...")

if text_input:
    doc = nlp(text_input)
    html = displacy.render(doc, style="ent", minify=True)
    st.markdown("### Entity Recognition")
    st.components.v1.html(html, scrolling=True, height=300)
