import pandas as pd

df = pd.read_csv("data/games_2020_2025.csv", index_col="name")
df = df.drop(columns=["id", "playtime", "ratings_count"])

print(df)