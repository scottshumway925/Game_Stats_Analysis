import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np
import matplotlib.pyplot as plt

with open("data/boardgamegeek.json", encoding="utf-8") as f:
    data = json.load(f)

rows = []
for game in data:

    # Getting the game's metadata
    mechanisms = game.get("game_info", {}).get("mechanisms", [])
    ratings = game.get("ratings", {})
    ownership_number = game.get("collection_stats", {}).get("own", 0)

    # Getting the rating count
    ratings_count = [ratings.get(f"rated_{i}", 0) for i in range(1, 11)]
    total_ratings = sum(ratings_count)

    # Weighted average calculation
    if total_ratings > 0:
        weighted_avg = sum(r * c for r, c in zip(range(1, 11), ratings_count)) / total_ratings
    else:
        weighted_avg = 0

    # Getting suggested retail price
    marketplace = game.get("marketplace", [])
    suggested_retail_price = next((entry.get("base_price_usd") for entry in marketplace if entry.get("store") == "Suggested retail"), 0.0)
    suggested_retail_price = float(suggested_retail_price)

    # Calculating the predicted revenue
    predicted_revenue = ownership_number * suggested_retail_price

    # Adding the rows to our list
    rows.append({
        "mechanisms": mechanisms,
        "average_game_rating": weighted_avg,
        "ownership": ownership_number,
        "suggested_retail_price": suggested_retail_price,
        "predicted_revenue": predicted_revenue
    })

df = pd.DataFrame(rows)
df = df.explode("mechanisms")

# Filtering out bad data
df = df[df["ownership"] > 0]
df = df[df["suggested_retail_price"] > 0]

# Converting all data types to numeric typing
df["ownership"] = pd.to_numeric(df["ownership"], errors="coerce")
df["predicted_revenue"] = pd.to_numeric(df["predicted_revenue"], errors="coerce")
df["average_game_rating"] = pd.to_numeric(df["average_game_rating"], errors="coerce")

df = df.dropna(subset=["ownership", "predicted_revenue", "average_game_rating"])

df_analysis = df.groupby("mechanisms").agg(
    mechanism_count=("mechanisms", "count"),
    game_rating_average=("average_game_rating", "mean"),
    average_revenue=("predicted_revenue", "mean")
).sort_values(by="mechanism_count", ascending=False)

print("=== Mechanism Summary ===")
print(df_analysis.head(10).to_string(formatters={"average_revenue": lambda x: f"{x:,.2f}", "game_rating_average": lambda x: f"{x:,.2f}"}))

x = pd.get_dummies(df[["ownership", "predicted_revenue", "mechanisms"]], columns=["mechanisms"])
y = df["average_game_rating"]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(x_train, y_train)

y_pred = model.predict(x_test)

r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print("\n=== Model Performance ===")
print(f"R² score: {r2:.3f}")
print(f"RMSE: {rmse:.3f}")

print("\n=== Model Coefficients ===")
for feature, coef in zip(x.columns, model.coef_):
    print(f"{feature}: {coef:.6f}")
print(f"Intercept: {model.intercept_:.3f}")

new_games = pd.DataFrame({
    "ownership": [1000, 20000, 100000],
    "predicted_revenue": [1000*50, 20000*60, 100000*80],
    "mechanisms": [["End Game bonuses", "Passed Action Token", "Paper-and-Pencil"], ["Market", "Order Counters", "Open Drafting"], ["Variable Setup", "Negotiation", "Multi-Use Cards"]]
})

new_games_exploded = new_games.explode("mechanisms")

new_games_encoded = pd.get_dummies(new_games_exploded, columns=["mechanisms"])
new_games_encoded = new_games_encoded.groupby(new_games_exploded.index).sum()
new_games_encoded["ownership"] = new_games["ownership"]
new_games_encoded["predicted_revenue"] = new_games["predicted_revenue"]
new_games_encoded = new_games_encoded.reindex(columns=x.columns, fill_value=0)

predictions = model.predict(new_games_encoded)

print("\n=== Predictions for New Games ===")
for i, p in enumerate(predictions):
    print(f"Game {i+1} predicted rating: {p:.2f}")