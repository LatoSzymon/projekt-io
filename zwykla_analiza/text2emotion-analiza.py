import pandas as pd
import text2emotion as te
import os
import nltk
nltk.download("punkt_tab")
from tqdm import tqdm
tqdm.pandas()

df = pd.read_csv("full_comments_translated.csv")
df = df.dropna(subset=["comment_en"])

def analyze_emotions(text):
    try:
        result = te.get_emotion(text)
        return pd.Series(result)
    except Exception as e:
        print("Błąd:", e)
        return pd.Series({"Happy": None, "Angry": None, "Surprise": None, "Sad": None, "Fear": None})

emotion_df = df["comment_en"].progress_apply(analyze_emotions)
df = pd.concat([df, emotion_df], axis=1)

output = "full_comments_text2emotion.csv"
if os.path.exists(output):
    os.remove(output)

df.to_csv(output, index=False)
print("TEXT2MOTION DONE")
