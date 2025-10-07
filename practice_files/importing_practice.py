import pandas as pd

df = pd.read_csv("pokemon_stats.csv", index_col="Name")

# Selection by column
print(df[["Height", "Weight"]].to_string())

# Selection by rows
print(df.loc["Charizard":"Blastoise", ["Height", "Weight"]])
print(df.iloc[0:11:2, 0:3])

pokemon = input("Enter a Pokemon name: ")

try:
    print(df.loc[pokemon])
except KeyError:
    print(f"{pokemon} not found")

df.head()
df.describe()
df.info()