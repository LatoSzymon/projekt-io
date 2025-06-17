import pandas as pd
import ast


tagged = pd.read_csv("C:/Users/Szymon/repo/projekt-io/sondaze/full_comments_tagged.csv")
pares = pd.read_csv("C:/Users/Szymon/repo/projekt-io/zwykla_analiza/full_comments_analyzed_1.csv")
vader = pd.read_csv("C:/Users/Szymon/repo/projekt-io/zwykla_analiza/full_comments_vader.csv")

tagged["candidates"] = tagged["candidates"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

def prepare_model_data(tagged_df, model_df, sentiment_column, model_name):
    merged = pd.merge(tagged_df, model_df[["comment_id", sentiment_column]], on="comment_id", how="inner")
    merged = merged.explode("candidates")
    merged = merged[merged[sentiment_column].isin(["Positive", "Negative", "Neutral", "positive", "negative", "neutral"])]

    merged[sentiment_column] = merged[sentiment_column].str.lower()

    grouped = (
        merged
        .groupby(["candidates", "phase", sentiment_column])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    grouped["total"] = grouped[["positive", "neutral", "negative"]].sum(axis=1)
    grouped["positive_ratio"] = (grouped["positive"] / grouped["total"]).round(3)
    
    output_file = f"poll_results_{model_name.lower()}.csv"
    grouped.to_csv(output_file, index=False)
    print(f"Wyniki zapisane: {output_file}")

prepare_model_data(tagged, pares, "political_sentiment", "PaReS")

prepare_model_data(tagged, vader, "vader_sentiment", "VADER")
