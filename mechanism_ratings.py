import pandas as pd
import json

pd.set_option('display.float_format', lambda x: '{:,.2f}'.format(x))

with open("data/boardgamegeek.json", encoding="utf-8") as f:
    data = json.load(f)

rows = []
for game in data:
    mechanisms = game.get("game_info", {}).get("mechanisms", [])
    ratings = game.get("ratings", {})
    ratings_count = [ratings.get(f"rated_{i}", 0) for i in range(1, 11)]
    ownership_number = game.get("collection_stats", {}).get("own", [])
    
    marketplace = game.get("marketplace", [])
    suggested_retail_price = next((entry.get("base_price_usd") for entry in marketplace if entry.get("store") == "Suggested retail"), 0.0)
    suggested_retail_price = float(suggested_retail_price)
    predicted_revenue = ownership_number * suggested_retail_price

    total_ratings = sum(ratings_count)
    if total_ratings > 0:
        weighted_avg = sum(r * c for r, c in zip(range(1, 11), ratings_count)) / total_ratings
    else:
        weighted_avg = 0

    if predicted_revenue != 0:
        rows.append({
            "mechanisms": mechanisms,
            "average_game_rating": weighted_avg,
            "ownership": ownership_number,
            "predicted_revenue": predicted_revenue
        })

df = pd.DataFrame(rows)

df = df.explode("mechanisms")
df = df[df["ownership"] > 10000]

df_analysis = df.groupby("mechanisms").agg(
    mechanism_count=("mechanisms", "count"),
    game_rating_average=("average_game_rating", "mean"),
    predicted_average_revenue=("predicted_revenue", "mean")
).sort_values(by="mechanism_count", ascending=False)

filtered_df = df_analysis[df_analysis["game_rating_average"] > 0]
filtered_df = filtered_df.round(2)

print(df_analysis.to_string())