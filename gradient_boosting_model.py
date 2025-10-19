import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np

# Load JSON
with open("data/boardgamegeek.json", encoding="utf-8") as f:
    data = json.load(f)

# Prepare rows
rows = []
for game in data:
    mechanisms = game.get("game_info", {}).get("mechanisms", [])
    # Replace None or empty with ["No Mechanism"]
    if not mechanisms:
        mechanisms = ["No Mechanism"]
    ratings = game.get("ratings", {})
    ownership_number = game.get("collection_stats", {}).get("own", 0)

    ratings_count = [ratings.get(f"rated_{i}", 0) for i in range(1, 11)]
    total_ratings = sum(ratings_count)
    weighted_avg = sum(r * c for r, c in zip(range(1, 11), ratings_count)) / total_ratings if total_ratings > 0 else 0

    marketplace = game.get("marketplace", [])
    suggested_retail_price = next((entry.get("base_price_usd") for entry in marketplace if entry.get("store") == "Suggested retail"), 0.0)
    suggested_retail_price = float(suggested_retail_price)
    predicted_revenue = ownership_number * suggested_retail_price

    rows.append({
        "mechanisms": mechanisms,
        "average_game_rating": weighted_avg,
        "ownership": ownership_number,
        "predicted_revenue": predicted_revenue
    })

df = pd.DataFrame(rows)

# Filter bad data
df = df[df["ownership"] > 0]
df = df[df["predicted_revenue"] > 0]

# Encode mechanisms using MultiLabelBinarizer
mlb = MultiLabelBinarizer()
mechanisms_encoded = pd.DataFrame(mlb.fit_transform(df["mechanisms"]),
                                  columns=[f"mechanism_{m}" for m in mlb.classes_],
                                  index=df.index)

X = pd.concat([df[["ownership", "predicted_revenue"]], mechanisms_encoded], axis=1)
y = df["average_game_rating"]

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Gradient Boosting model
model = GradientBoostingRegressor(random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("=== Model Performance (Gradient Boosting) ===")
print(f"R² score: {r2:.3f}")
print(f"RMSE: {rmse:.3f}")

# Example: new games
new_games = pd.DataFrame({
    "ownership": [1000, 20000, 100000],
    "predicted_revenue": [1000*50, 20000*60, 100000*80],
    "mechanisms": [
        ["Variable Set-up", "Negotiation", "Multi-Use Cards"],
        ["End Game Bonuses", "Passed Action Token", "Paper-and-Pencil"],
        ["Market", "Order Counters", "Open Drafting"]
    ]
})

# Encode new games using same encoder
mechanisms_new_encoded = pd.DataFrame(
    mlb.transform(new_games["mechanisms"]),
    columns=[f"mechanism_{m}" for m in mlb.classes_]
)
X_new = pd.concat([new_games[["ownership", "predicted_revenue"]], mechanisms_new_encoded], axis=1)

predictions = model.predict(X_new)
print("\n=== Predictions for New Games ===")
for i, p in enumerate(predictions):
    print(f"Game {i+1} predicted rating: {p:.2f}")
