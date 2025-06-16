import pandas as pd
from transformers import pipeline
import os

df = pd.read_csv("full_comments.csv")
df = df.dropna(subset=["comment_text"])

nlp = pipeline("sentiment-analysis",
               model="nlptown/bert-base-multilingual-uncased-sentiment",
               tokenizer="nlptown/bert-base-multilingual-uncased-sentiment")

def analiza(text):
    try:
        result = nlp(text[:512])
        return result[0]["label"]
    except Exception as erere:
        print("BŁĄD", erere)
        return "error"
    
if os.path.exists("full_comments_nlptown.csv"):
     os.remove("full_comments_nlptown.csv")
     print("Plik został usunięty przed rozpoczęciem zapisu.")
     
df["nlptown_sentiment"] = df["comment_text"].apply(analiza)

original = pd.read_csv("full_comments.csv")[["comment_id", "phase"]]
df = df.merge(original, on="comment_id", how="left")

df.to_csv("full_comments_nlptown.csv", index=False)
print("ANALIZA NLPtown ZAKOŃCZONA")


