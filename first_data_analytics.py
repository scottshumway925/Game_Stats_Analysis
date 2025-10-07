import pandas as pd

df = pd.read_csv("data/rawg_games.csv", index_col="name")
df = df.drop(columns=["platforms", "id", "playtime", "released", "rating", "ratings_count"])

print(df.to_string())