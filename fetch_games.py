import requests
import pandas as pd

API_KEY = "03bfb17b7f324dda867375cd75d0e615"
BASE_URL = "https://api.rawg.io/api/games"

def fetch_games(page_size=40, pages=5):
    all_games = []
    for page in range(1, pages + 1):
        params = {
            "key": API_KEY,
            "page_size": page_size,
            "page": page,
            "ordering": "-metacritic"
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        for g in data.get("results", []):
            all_games.append({
                "id": g.get("id"),
                "name": g.get("name"),
                "released": g.get("released"),
                "rating": g.get("rating"),
                "ratings_count": g.get("ratings_count"),
                "metacritic": g.get("metacritic"),
                "playtime": g.get("playtime"),
                "genres": ", ".join([genre["name"] for genre in g.get("genres", [])]),
                "platforms": ", ".join([p["platform"]["name"] for p in g.get("platforms", [])])
            })
        
        print(f"Fetched page {page}")

    return pd.DataFrame(all_games)

if __name__ == "__main__":
    df = fetch_games(page_size=40, pages=5)
    df.to_csv("data/rawg_games.csv", index=False)
    print(f"saved {len(df)} games to data/rawg_games.csv")