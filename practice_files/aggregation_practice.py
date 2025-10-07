import pandas as pd

df = pd.read_csv("pokemon_stats.csv", index_col="Name")

# Applies to the whole dataframe
print(df.mean(numeric_only=True))
print(df.sum(numeric_only=True))
print(df.min(numeric_only=True))
print(df.max(numeric_only=True))
print(df.count())

# Applies to a single column
print(df["Height"].mean())
print(df["Height"].sum())
print(df["Height"].min())
print(df["Height"].max())
print(df["Height"].count())

group = df.groupby("Type1")
print(group["Height"].mean())
print(group["Height"].sum())
print(group["Height"].min())
print(group["Height"].max())
print(group["Height"].count())