import pandas as pd
from textblob import TextBlob
import os

df = pd.read_csv("full_comments_translated.csv")
df = df.dropna(subset=["comment_en"])

def analiza_blob(text):
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        if polarity > 0.05:
            label = "positive"
        elif polarity < -0.05:
            label = "negative"
        else:
            label = "neutral"
            
        return pd.Series([polarity, subjectivity, label])

    except:
        return pd.Series([None, None, "error"])
    
df[["tb_polarity", "tb_subjectivity", "tb_sentiment"]] = df["comment_en"].apply(analiza_blob)

output = "full_comments_textblob.csv"
if os.path.exists(output):
    os.remove(output)

df.to_csv(output, index=False)
print("TextBlob analiza zakończona")