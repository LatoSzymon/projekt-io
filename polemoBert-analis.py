import pandas as pd
from transformers import pipeline
import os

df = pd.read_csv("full_comments.csv")
df = df.dropna(subset=["comment_text"])

nlp = pipeline("sentiment-analysis",
               model="dfurmanek/PolEmo2.0-bert-base-polemo2",
               tokenizer="dfurmanek/PolEmo2.0-bert-base-polemo2")

def analyze(text):
    try:
        result = nlp(text[:512])[0]
        return result["label"]
    except Exception as e:
        print("Błąd:", e)
        return "error"

output = "full_comments_polemo.csv"
if os.path.exists(output):
    os.remove(output)

df["polemo_sentiment"] = df["comment_text"].apply(analyze)
df.to_csv(output, index=False)
print("BERT")
