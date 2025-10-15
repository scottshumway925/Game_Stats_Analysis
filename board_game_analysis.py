import pandas as pd
import json

with open("data/boardgamegeek.json", encoding="utf-8") as f:
    data = json.load(f)

rows = []
for game in data:
    boardgame_name = game.get("boardgame")
    mechanisms = game.get("game_info", {}).get("mechanisms", [])
    ownership_number = game.get("collection_stats", {}).get("own", [])

    ratings = game.get("ratings", {})
    rating_counts = [ratings.get(f"rated_{i}", 0) for i in range(1, 11)]

    total_ratings = sum(rating_counts)
    if total_ratings > 0:
        weighted_avg = sum(r * c for r, c in zip(range(1, 11), rating_counts)) / total_ratings
    else:
        weighted_avg = 0

    rows.append({
        "boardgame": boardgame_name,
        "mechanisms": mechanisms,
        "ownership_numbers": ownership_number,
        "average_rating": weighted_avg
    })

df = pd.DataFrame(rows)

df = df.explode("mechanisms")

df_analysis = df.groupby("boardgame").agg(
    average_rating=("average_rating", "mean"),
    average_ownership=("ownership_numbers", "mean"),
    complexity_count=("mechanisms", "count"),
    mechanisms=("mechanisms", lambda s: ", ".join(sorted({m for m in s if pd.notna(m)})))
).sort_values(by="average_rating", ascending=False)

df_analysis["mechanisms"] = df_analysis["mechanisms"].fillna("")

filtered_db = df_analysis[df_analysis["average_rating"] >= 8]
filtered_db = filtered_db[filtered_db["average_ownership"] >= 10000]
filtered_db = filtered_db.round(2)

print(filtered_db[["average_rating", "average_ownership", "mechanisms"]].to_string())
