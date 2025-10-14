import pandas as pd
import json

with open("data/boardgamegeek.json", encoding="utf-8") as f:
    data = json.load(f)

rows = []
for game in data:
    boardgame_name = game.get("boardgame")
    mechanisms = game.get("game_info", {}).get("mechanisms", [])
    ownership_number = game.get("collection_stats", {}).get("own", [])

    rows.append({
        "boardgame": boardgame_name,
        "mechanisms": mechanisms,
        "ownership_numbers": ownership_number
    })

df = pd.DataFrame(rows)

df = df.explode("mechanisms")

df_grouped = df.groupby("mechanisms").agg(
    game_count=("mechanisms", "count"),
    average_ownership=("ownership_numbers", "mean")
).sort_values(by="game_count", ascending=False)


df_grouped = df_grouped.round(0).astype(int)
print(df_grouped.to_string())
