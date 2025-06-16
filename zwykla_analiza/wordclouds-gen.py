import pandas as pd
import nltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from nltk.corpus import stopwords

nltk.download("stopwords")
polish_stopwords = set("""
a które jako bez prostu który tych cię tyrant https tym czasu simiona może tyle jakoś reddit można lat chce takie która pjpg auto preview sie będą aby ach aj albo ale tym ani aż bardzo bo bowiem by był była było byli być ci cie ciebie co cokolwiek coś czy czyli daleko dla dlaczego dlatego do dobrze dokąd dość dużo gdzie go gdy gdyby gdyż i ich ile im inna inne inny iż ja jak jakaś jakiś ją je jeden jednak jego jej jemu jest jestem jeszcze jeśli już ją każdy kiedy kim kto ku lecz lub ma mają mam mnie mogą moje moim musi my na nad nam nami nas nasze nasz naście natomiast natychmiast nawet ni niż nic nich nie niej nią nim nimi niż no o obok od około on ona one oni ono oraz oto ponieważ pod podczas potem poza prawie przecież przed przede przez przy roku sama same samemu sobie sobą są ta tak taka taki tam te tego tej ten teraz też to tobą tobie tutaj tu twoi twoim twój ty u w wam was wasz wasza wasze we więc więcej wiele wszyscy wszystko wszystkie wszystkich się z za zawsze ze siebie sobie sobą że żeby
""".split())

#UWAGA! Niniejszy kod zawiera słowa wysoce niecenzuralne. Twórca kodu nie ponosi żadnej odpowiedzialności za ewentualną demoralizację i zgorszenie wywołane prezentowanym kodem. Przed użyciem zapoznaj się z treścią ulotki nie dołączonej do projektu bądź skonsultuj się z lekarzem lub farmaceutą.
custom_blocklist = polish_stopwords.union({
    "pan", "pani", "to", "tego", "jest", "czy", "jak", "tylko", "trzeba",
    "mam", "bo", "by", "ale", "został", "będzie", "mnie", "było",
    "kurwa", "chuj", "jebany", "pierdol", "spierdalaj", "zjeb", "dziwka", "kutas", "cwel"
})

df = pd.read_csv("full_comments.csv")
df = df.dropna(subset=["comment_text"])

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-ząćęłńóśżź ]", " ", text)
    words = text.split()
    words = [w for w in words if w not in custom_blocklist and len(w) > 2]
    return " ".join(words)

for phase in ["pre", "between", "post"]:
    phase_text = df[df["phase"] == phase]["comment_text"].dropna().apply(clean_text)
    combined_text = " ".join(phase_text)

    wordcloud = WordCloud(width=1000, height=600, background_color="white").generate(combined_text)

    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"WordCloud – Faza: {phase.upper()}", fontsize=16)
    plt.tight_layout()
    plt.savefig(f"wordcloud_{phase}.png")
    plt.show()
