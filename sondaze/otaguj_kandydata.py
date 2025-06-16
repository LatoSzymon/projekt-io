import pandas as pd
import re

df = pd.read_csv("C:/Users/Szymon/repo/projekt-io/zwykla_analiza/full_comments.csv")
df = df.dropna(subset=["comment_text"])

kandydaci = {
    "Trzaskowski": ["trzaskowski", "rafał", "rafal trzaskowski", "tusk", "platforma", "ko"],
    "Nawrocki": ["nawrocki", "karol", "karol nawrocki", "pis", "kaczyński"],
    "Mentzen": ["mentzen", "sławomir", "sławek", "sławomir mentzen", "konfederacja"],
    "Hołownia": ["hołownia", "szymon", "szymon hołownia", "2050"],
    "Braun": ["braun", "grzegorz", "grzegorz braun"],
    "Zandberg": ["zandberg", "adrian", "adrian zandberg", "duńczyk", "razem"],
    "Biejat": ["biejat", "magdalena", "magdalena biejat", "lewica"],
    "Senyszyn": ["senyszyn", "joanna", "joanna senyszyn"],
    "Jakubiak": ["jakubiak", "marek", "marek jakubiak", "sarmata"],
    "Bartoszewicz": ["bartoszewicz", "bartosiewicz", "artur", "bartoszewicz", "bezpartyjni samorządowcy"],
    "Maciak": ["maciak", "maciej", "maciej maciak"],
    "Woch": ["woch", "marek", "marek woch"],
    "Stanowski": ["stanowski", "krzysztof", "krzysztof stanowski"]
}

def przypisz_kandydatow(text):
    text = text.lower()
    znalezieni = []
    for kandydat, slowa in kandydaci.items():
        if any(re.search(rf"\b{re.escape(s)}\b", text) for s in slowa):
            znalezieni.append(kandydat)
    return znalezieni if znalezieni else None

df["candidates"] = df["comment_text"].apply(przypisz_kandydatow)

df_tagged = df[df["candidates"].notna()]
df_tagged.to_csv("full_comments_tagged.csv", index=False)
print("Komentarze przypisane do kandydatów")
