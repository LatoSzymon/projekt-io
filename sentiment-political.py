import pandas as pd
from transformers import pipeline
import os

df = pd.read_csv("full_comments.csv")
df = df.dropna(subset=["comment_text"])

nlp = pipeline("sentiment-analysis",
               model="eevvgg/PaReS-sentimenTw-political-PL",
               tokenizer="eevvgg/PaReS-sentimenTw-political-PL")

def analiza(text):
    try:
        result = nlp(text[:512])
        return result[0]["label"]
    except Exception as erere:
        print("BŁĄD", erere)
        return "error"
    
if os.path.exists("full_comments_analyzed_1.csv"):
     os.remove("full_comments_analyzed_1.csv")
     print("Plik z tłumaczeniami został usunięty przed rozpoczęciem zapisu.")
     
     
df["political_sentiment"] = df["comment_text"].apply(analiza)


df.to_csv("full_comments_analyzed_1.csv", index=False)
print("ANAL I ZA SKOŃCZONA")