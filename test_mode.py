import spacy

nlp = spacy.load("src/trainer/output/model-best")

text = "Apr 29 07:21:01 example-server CRON[42069]: pam_unix(cron:session): session opened for user root by (uid=0)"
doc = nlp(text)

for ent in doc.ents:
    print(ent.text, ent.label_)