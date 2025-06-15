import pandas as pd
from deep_translator import GoogleTranslator
from time import sleep
import os

df = pd.read_csv("full_comments.csv")

unikalne_komenty = df["comment_text"].dropna().unique()

tlumaczenia = {}
print(len(unikalne_komenty), " to liczba unikalnych komentarzy")

for i, text in enumerate(unikalne_komenty):
    try:
        tlumacz = GoogleTranslator(source="pl", target="en").translate(text)
        tlumaczenia[text] = tlumacz
        print("przetłumaczono komentarz: ", i)
        sleep(0.5)
    except Exception as errorus:
        print("Błąd przy tłumaczaniu", errorus)
        tlumaczenia[text] = ""
        

if os.path.exists("full_comments_translated.csv"):
     os.remove("full_comments_translated.csv")
     print("Plik z tłumaczeniami został usunięty przed rozpoczęciem zapisu.")
    

df["comment_en"] = df["comment_text"].map(tlumaczenia)

df.to_csv("full_comments_translated.csv", index=False)
print("TŁUMACZENIE DONE")