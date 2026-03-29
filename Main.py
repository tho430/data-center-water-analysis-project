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
plt.savefig("plots/q2_bar.png")
plt.clf()

print("\nSummary:")
print(
    f"- Water use: {df.iloc[0]['water_consumption_billion_gallons']} -> "
    f"{df.iloc[-1]['water_consumption_billion_gallons']} billion gallons"
)
print(
    f"- Replenishment: {df.iloc[0]['replenishment_percent']}% -> "
    f"{df.iloc[-1]['replenishment_percent']}%"
)

corr = df[["water_consumption_billion_gallons", "replenishment_percent"]].corr()
print(corr)

plt.imshow(corr, cmap='coolwarm', interpolation='none')
plt.colorbar()
plt.xticks([0,1], corr.columns)
plt.yticks([0,1], corr.columns)
plt.title("Correlation Matrix")
plt.clf()

plt.scatter(df["water_consumption_billion_gallons"], df["replenishment_percent"])
plt.title("Water Consumption vs Replenishment Percentage")
plt.xlabel("Water Consumption (Billions of Gallons)")
plt.ylabel("Replenishment (%)")
plt.savefig("plots/Consumption_VS_Replenishment_Percentage.png")
plt.show()
plt.clf()

plt.plot(df["year"], df["water_consumption_billion_gallons"], label="Water Consumption")
plt.plot(df["year"], df["replenishment_percent"], label="Replenishment %")
plt.title("Water Consumption vs Replenishment Over Time")
plt.xlabel("Year")
plt.ylabel("Values")
plt.savefig("plots/Consumption_VS_Replenishment_Time.png")
plt.legend()
ply.show()
plt.clf()