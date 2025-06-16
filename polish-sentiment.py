import pandas as pd
from transformers import pipeline
import os

df = pd.read_csv("full_comments.csv")
df = df.dropna(subset=["comment_text"])

nlp = pipeline("sentiment-analysis",
               model="eevvgg/bert-polish-sentiment-politics",
               tokenizer="eevvgg/bert-polish-sentiment-politics")

def analyze(text):
    try:
        res = nlp(text[:512])[0]
        return res["label"]
    except Exception as e:
        print("Błąd:", e)
        return "error"

out = "full_comments_eevvgg.csv"
if os.path.exists(out):
    os.remove(out)

df["eevvgg_sentiment"] = df["comment_text"].apply(analyze)

original = pd.read_csv("full_comments.csv")[["comment_id", "phase"]]
df = df.merge(original, on="comment_id", how="left")

df.to_csv("full_comments_eevvgg.csv", index=False)
print("ANALIZA EEVVGG ZAKOŃCZONA")


