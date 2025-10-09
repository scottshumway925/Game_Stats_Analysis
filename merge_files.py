import pandas as pd

rawg_df = pd.read_csv("data/rawg_games.csv")
steam_df = pd.read_csv("data/steamspy_2020.csv")

merged_df = pd.merge(rawg_df, steam_df, on="name", how="inner")
merged_df.to_csv("data/merged_2020_games.csv", index=False)

print(f"Merged {len(merged_df)} games from RAWG and SteamSpy.")
