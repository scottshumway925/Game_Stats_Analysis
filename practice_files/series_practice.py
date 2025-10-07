import numpy as np
import pandas as pd

data = [1, 3, 5, 7, 9]

series = pd.Series(data, index=["a", "b", "c", "d", "e"])

series.loc["c"] = 17

print(series[series >= 8])

print("\n")

calories = {"Day 1": 1750, "Day 2": 2100, "Day 3": 1700}

series2 = pd.Series(calories)

print(series2)
print(series2.loc["Day 3"])

series2.loc["Day 3"] += 500

print(series2)