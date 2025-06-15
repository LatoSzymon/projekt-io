import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="whitegrid")

sources = [
    ("PaReS", "full_comments_analyzed_1.csv", "political_sentiment"),
    ("eevvgg", "full_comments_eevvgg.csv", "eevvgg_sentiment"),
    ("VADER", "full_comments_vader.csv", "vades_sentiment"),
    ("TextBlob", "full_comments_textblob.csv", "tb_sentiment")
]

valid_sentiments = {"positive", "neutral", "negative"}

for model_name, filepath, column in sources:
    try:
        df = pd.read_csv(filepath)
        if column not in df.columns or "phase" not in df.columns:
            print(f"Pominięto {model_name}: brak kolumny '{column}' lub 'phase'")
            continue

        df = df[df[column].isin(valid_sentiments)]
        summary = df.groupby(["phase", column]).size().reset_index(name="count")

        plt.figure(figsize=(8, 5))
        sns.barplot(data=summary, x="phase", y="count", hue=column, palette="Set2")
        plt.title(f"Sentiment wg faz – model {model_name}")
        plt.xlabel("Faza kampanii")
        plt.ylabel("Liczba komentarzy")
        plt.legend(title="Sentyment")
        plt.tight_layout()
        plt.savefig(f"{model_name.lower()}_sentiment_by_phase.png")
        plt.show()

    except FileNotFoundError:
        print(f"Nie znaleziono pliku: {filepath}")
    except Exception as e:
        print(f"Błąd przy przetwarzaniu {model_name}: {e}")

try:
    df_emotion = pd.read_csv("full_comments_text2emotion.csv")
    if "phase" not in df_emotion.columns:
        print("⚠️ Plik z emocjami nie zawiera kolumny 'phase'")
    else:
        emotions = ["Happy", "Angry", "Surprise", "Sad", "Fear"]
        for emotion in emotions:
            if emotion not in df_emotion.columns:
                print(f"⚠️ Brak kolumny: {emotion}")
                continue

            emotion_summary = df_emotion.groupby("phase")[emotion].mean().reset_index()

            plt.figure(figsize=(6, 4))
            sns.barplot(data=emotion_summary, x="phase", y=emotion, palette="coolwarm")
            plt.title(f"Średni poziom emocji: {emotion}")
            plt.ylabel("Średnia wartość [0–1]")
            plt.xlabel("Faza kampanii")
            plt.ylim(0, 1)
            plt.tight_layout()
            plt.savefig(f"emotion_{emotion.lower()}_by_phase.png")
            plt.show()

except FileNotFoundError:
    print("Nie znaleziono pliku: full_comments_text2emotion.csv")
except Exception as e:
    print(f"Błąd przy przetwarzaniu emocji: {e}")
