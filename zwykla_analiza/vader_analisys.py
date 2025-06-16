import pandas as pd
print(pd.__file__)
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download("vader_lexicon")

df = pd.read_csv("full_comments_translated.csv")
df = df.dropna(subset=["comment_en"])

sia = SentimentIntensityAnalyzer()

def analiza(text):
    try:
        return sia.polarity_scores(text)
    except:
        return {"neg": None, "neu": None, "pos": None, "compound": None}
    
vader_scores = df["comment_en"].apply(analiza).apply(pd.Series)

def klasyfikacja(compound):
    if pd.isna(compound):
        return "error"
    elif compound >= 0.05:
        return "positive"
    elif compound <= -0.05:
        return "negative"
    else:
        return "neutral"
    
vader_scores["vades_sentiment"] = vader_scores["compound"].apply(klasyfikacja)

df = pd.concat([df, vader_scores], axis=1)

if os.path.exists("full_comments_vader.csv"):
    os.remove("full_comments_vader.csv")
    print("Aborcja przed analizą")
    
df.to_csv("full_comments_vader.csv", index=False)
print("DARTH VADER HAS ARRIVED")