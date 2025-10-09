import requests
import pandas as pd
import time

def fetch_steamspy_all():
    """Fetch all games listed on SteamSpy (basic info only)."""
    url = "https://steamspy.com/api.php"
    params = {"request": "all"}
    response = requests.get(url, params=params)
    data = response.json()

    games = []
    for appid, info in data.items():
        games.append({
            "appid": appid,
            "name": info.get("name"),
            "developer": info.get("developer"),
            "publisher": info.get("publisher"),
            "owners": info.get("owners"),
            "average_forever": info.get("average_forever"),
            "price": info.get("price"),
            "score_rank": info.get("score_rank")
        })
    return pd.DataFrame(games)

def fetch_release_date(appid):
    """Fetch release date for a given Steam App ID."""
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        info = data.get(str(appid), {}).get("data", {})
        if info and "release_date" in info and info["release_date"]["date"]:
            return info["release_date"]["date"]
    except Exception:
        return None
    return None

def filter_steam_games_2020(limit=300):
    """Fetch and filter Steam games released in 2020."""
    all_games = fetch_steamspy_all()
    print(f"Fetched {len(all_games)} total games from SteamSpy.")
    
    # To avoid overloading the API, limit how many we check
    all_games = all_games.head(limit)

    filtered = []
    for i, row in all_games.iterrows():
        appid = row["appid"]
        release_date = fetch_release_date(appid)
        if release_date and any(y in release_date for y in ["2020", "2021", "2022", "2023", "2024", "2025"]):
            row["release_date"] = release_date
            filtered.append(row)
            print(f"✅ {row['name']} ({release_date})")
        else:
            print(f"⏭️ Skipped {row['name']} ({release_date})")

    df = pd.DataFrame(filtered)
    df.to_csv("data/steamspy_2020.csv", index=False)
    print(f"Saved {len(df)} games released in 2020 to data/steamspy_2020.csv")
    return df

if __name__ == "__main__":
    df_2020 = filter_steam_games_2020(limit=10000)