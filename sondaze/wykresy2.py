import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

pares = pd.read_csv("poll_results_pares.csv")
vader = pd.read_csv("poll_results_vader.csv")


def przygotuj_i_rysuj(df, model_name, color):
    df_summary = df.groupby("candidates")["positive"].sum().reset_index()

    total_positive = df_summary["positive"].sum()
    df_summary["support_percent"] = (df_summary["positive"] / total_positive * 100).round(2)

    df_summary = df_summary.sort_values(by="support_percent", ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_summary, x="candidates", y="support_percent", color=color)
    plt.title(f"Symulowane poparcie ({model_name})")
    plt.xlabel("Kandydat")
    plt.ylabel("Udział pozytywnych komentarzy [%]")
    plt.xticks(rotation=60, ha="right")

    plt.tight_layout()
    filename = f"sondaz_poparcie_{model_name.lower()}.png"
    plt.savefig(filename)
    plt.close()
    print(f"Zapisano wykres: {filename}")

przygotuj_i_rysuj(pares, "PaReS", "#325ed6")
przygotuj_i_rysuj(vader, "VADER", "#e41515")