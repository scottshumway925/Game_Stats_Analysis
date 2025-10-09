import pandas as pd

df = pd.read_csv("data/games_2020_2025.csv", index_col="name")
df = df.drop(columns=["id", "ratings_count"])

df = df[df["metacritic"] > 0]

df["genres"] = df["genres"].str.split(", ")
df = df.explode("genres")

genre_stats = df.groupby("genres").agg(
    game_count=("genres", "count"),
    avg_playtime_hrs=("playtime", "mean"),
    avg_metacritic=("metacritic", "mean"),
    avg_rating=("rating", "mean")
).sort_values(by="game_count", ascending=False)


print()
print(genre_stats)