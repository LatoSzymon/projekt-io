import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

sns.set(style="whitegrid")

sources = [
    ("PaReS", "full_comments_analyzed_1.csv", "political_sentiment"),
    ("eevvgg - bert", "full_comments_eevvgg.csv", "eevvgg_sentiment"),
    ("VADER", "full_comments_vader.csv", "vades_sentiment"),
    ("TextBlob", "full_comments_textblob.csv", "tb_sentiment")
]

valid_sentiments = {"positive", "neutral", "negative"}

phase_order = ["pre", "between", "post"]
phase_labels = {
    "pre": "Przed I turą",
    "between": "Między turami",
    "post": "Po II turze"
}

for model_name, filepath, column in sources:
    try:
        if not os.path.exists(filepath):
            print(f"Nie ma pliku: {filepath}")
            continue

        df = pd.read_csv(filepath)
        if column not in df.columns:
            print(f"Pominięto {model_name}: brak '{column}'")
            continue
        if "phase" not in df.columns:
            print(f"Pominięto {model_name}: brak kolumny 'phase'")
            continue

        df[column] = df[column].str.lower()
        df = df[df[column].isin(valid_sentiments)]
        df["phase"] = pd.Categorical(df["phase"], categories=phase_order, ordered=True)
        df["phase_label"] = df["phase"].map(phase_labels)

        summary = df.groupby(["phase_label", column]).size().reset_index(name="count")

        plt.figure(figsize=(8, 5))
        sns.barplot(data=summary, x="phase_label", y="count", hue=column, palette="Set2")
        plt.title(f"Sentiment wg faz – model {model_name}")
        plt.xlabel("Faza kampanii")
        plt.ylabel("Liczba komentarzy")
        plt.legend(title="Sentyment")
        plt.tight_layout()
        output_path = f"{model_name.lower()}_sentiment_by_phase.png"
        plt.savefig(output_path)
        print(f"Zapisano wykres: {output_path}")
        plt.close()

    except Exception as e:
        print(f"Błąd przy przetwarzaniu {model_name}: {e}")

try:
    emotions_file = "full_comments_text2emotion.csv"
    if not os.path.exists(emotions_file):
        print(f"Nie znaleziono pliku: {emotions_file}")
    else:
        df_emotion = pd.read_csv(emotions_file)
        if "phase" not in df_emotion.columns:
            print("Plik z emocjami nie zawiera kolumny 'phase'")
        else:
            df_emotion["phase"] = pd.Categorical(df_emotion["phase"], categories=phase_order, ordered=True)
            df_emotion["phase_label"] = df_emotion["phase"].map(phase_labels)

            emotions = ["Happy", "Angry", "Surprise", "Sad", "Fear"]
            for emotion in emotions:
                if emotion not in df_emotion.columns:
                    print(f"Brak kolumny: {emotion}")
                    continue

                emotion_summary = df_emotion.groupby("phase_label")[emotion].mean().reset_index()

                plt.figure(figsize=(6, 4))
                sns.barplot(data=emotion_summary, x="phase_label", y=emotion, palette="coolwarm")
                plt.title(f"Średni poziom emocji: {emotion}")
                plt.ylabel("Średnia wartość [0–1]")
                plt.xlabel("Faza kampanii")
                plt.ylim(0, 1)
                plt.tight_layout()
                out_path = f"emotion_{emotion.lower()}_by_phase.png"
                plt.savefig(out_path)
                print(f"Zapisano wykres emocji: {out_path}")
                plt.close()

except Exception as e:
    print(f"Błąd przy przetwarzaniu emocji: {e}")

try:
    df_nlp = pd.read_csv("full_comments_nlptown.csv")
    if "nlptown_sentiment" not in df_nlp.columns or "phase" not in df_nlp.columns:
        print("Brak wymaganych kolumn w NLPtown")
    else:
        valid_nlptown = [f"{i} star" if i == 1 else f"{i} stars" for i in range(1, 6)]
        df_nlp = df_nlp[df_nlp["nlptown_sentiment"].isin(valid_nlptown)]

        df_nlp["phase"] = pd.Categorical(df_nlp["phase"], categories=phase_order, ordered=True)
        df_nlp["phase_label"] = df_nlp["phase"].map(phase_labels)

        summary_nlp = df_nlp.groupby(["phase_label", "nlptown_sentiment"]).size().reset_index(name="count")

        plt.figure(figsize=(8, 5))
        sns.barplot(
            data=summary_nlp,
            x="phase_label",
            y="count",
            hue="nlptown_sentiment",
            hue_order=valid_nlptown,
            palette="Set3"
        )
        plt.title("Sentiment wg faz – model NLPtown (1–5 gwiazdek)")
        plt.xlabel("Faza kampanii")
        plt.ylabel("Liczba komentarzy")
        plt.legend(title="Ocena")
        plt.tight_layout()
        plt.savefig("nlptown_sentiment_by_phase.png")
        print("Zapisano wykres: nlptown_sentiment_by_phase.png")
        plt.close()
except FileNotFoundError:
    print("Nie znaleziono pliku: full_comments_nlptown.csv")
except Exception as e:
    print(f"Błąd przy przetwarzaniu NLPtown: {e}")

