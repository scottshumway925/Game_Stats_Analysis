import os
import requests
import pandas as pd
import time

API_KEY = "03bfb17b7f324dda867375cd75d0e615"
BASE_URL = "https://api.rawg.io/api/games"

def fetch_games_by_date(start_date="2020-01-01", end_date="2025-12-31", pages=100, delay=1.0):
    all_games = []
    for page in range(1, pages + 1):
        params = {
            "key": API_KEY,
            "page_size": 50,
            "page": page,
            "ordering": "-metacritic",
            "dates": f"{start_date},{end_date}",
        }

        print(f"Fetching page {page} ({start_date}–{end_date})...")

        # Try 3 times before giving up
        for attempt in range(3):
            try:
                response = requests.get(BASE_URL, params=params, timeout=10)
                if response.status_code == 200:
                    break  # success, move on
                else:
                    print(f"Error {response.status_code}, attempt {attempt+1}/3...")
                    time.sleep(3)
            except requests.exceptions.RequestException as e:
                print(f"Network error: {e}, retrying...")
                time.sleep(3)
        else:
            print("Failed to fetch this page after 3 attempts — skipping.")
            continue

        data = response.json()
        results = data.get("results", [])
        if not results:
            print("No more results found — stopping.")
            break

        for g in results:
            all_games.append({
                "id": g.get("id"),
                "name": g.get("name"),
                "released": g.get("released"),
                "rating": g.get("rating"),
                "ratings_count": g.get("ratings_count"),
                "metacritic": g.get("metacritic"),
                "playtime": g.get("playtime"),
                "genres": ", ".join([genre["name"] for genre in g.get("genres") or []]),
                "platforms": ", ".join([p["platform"]["name"] for p in g.get("platforms") or []]),
            })

        if not data.get("next"):
            print("Reached last page of results.")
            break

        time.sleep(delay)

    return pd.DataFrame(all_games)


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    df = fetch_games_by_date("2020-01-01", "2025-12-31", pages=500)
    df.to_csv("data/games_2020_2025.csv", index=False)
    print(f"✅ Saved {len(df)} games released between 2020–2025 to data/games_2020_2025.csv")
