import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Data/google_water_usage")

print("Shape:", df.shape)
print("\nDtypes:\n", df.dtypes)
print("\nHead:\n", df.head().to_string(index=False))
print("\nMissing values:\n", df.isna().sum())
print("\nDescribe:\n", df.describe())

print("\nQuestions:")
print("1. How does water use change over time?")

os.makedirs("plots", exist_ok=True)

plt.plot(df["year"], df["water_consumption_billion_gallons"], marker="o")
plt.title("Water Use Over Time")
plt.xlabel("Year")
plt.ylabel("Billion Gallons")
plt.savefig("plots/q1_line.png")
plt.clf()

plt.figure(figsize=(8,5))
plt.bar(df["year"], df["replenishment_percent"])
plt.title("Water Replenishment Percentage Over Time")
plt.xlabel("Year")
plt.ylabel("Replenishment (%)")
plt.show()
plt.savefig("plots/q2_bar.png")


print("\nSummary:")
print(
    f"- Water use: {df.iloc[0]['water_consumption_billion_gallons']} -> "
    f"{df.iloc[-1]['water_consumption_billion_gallons']} billion gallons"
)
print(
    f"- Replenishment: {df.iloc[0]['replenishment_percent']}% -> "
    f"{df.iloc[-1]['replenishment_percent']}%"
)
