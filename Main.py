import csv
import os
from io import StringIO

import pandas as pd

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    matplotlib = None
    plt = None


DATA_PATHS = [
    "Data/google_water_usage.csv",
    "Data/google_water_usage",
]
EXPECTED_COLUMNS = [
    "year",
    "water_consumption_billion_gallons",
    "replenishment_percent",
    "notes",
]


def load_water_usage_data() -> pd.DataFrame:
    last_error = None

    for path in DATA_PATHS:
        if not os.path.exists(path):
            continue

        try:
            df = pd.read_csv(path)
            if set(EXPECTED_COLUMNS).issubset(df.columns):
                return normalize_dataframe(df)
        except Exception as exc:
            last_error = exc

        try:
            with open(path, "r", encoding="utf-8") as file:
                raw_text = file.read().strip()
            df = parse_malformed_csv(raw_text)
            if set(EXPECTED_COLUMNS).issubset(df.columns) and not df.empty:
                return normalize_dataframe(df)
        except Exception as exc:
            last_error = exc

    raise RuntimeError(f"Unable to load water usage data from {DATA_PATHS}: {last_error}")



def parse_malformed_csv(raw_text: str) -> pd.DataFrame:
    lines = [line.strip().strip('"') for line in raw_text.splitlines() if line.strip()]
    if not lines:
        raise ValueError("The input data file is empty.")

    reader = csv.reader(StringIO("\n".join(lines)))
    rows = list(reader)
    header = [column.strip() for column in rows[0]]

    normalized_rows = []
    for row in rows[1:]:
        if len(row) == 3:
            year, water, notes = row
            replenishment = None
        elif len(row) == 4:
            year, water, replenishment, notes = row
        elif len(row) >= 5:
            year = row[0]
            water = f"{row[1]}.{row[2]}"
            replenishment = row[3]
            notes = ",".join(row[4:])
        else:
            raise ValueError(f"Unexpected row format: {row}")

        normalized_rows.append([year, water, replenishment, notes])

    return pd.DataFrame(normalized_rows, columns=header)



def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [column.strip().strip('"') for column in df.columns]

    for column in ["year", "water_consumption_billion_gallons", "replenishment_percent"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df["notes"] = df["notes"].fillna("")
    return df.sort_values("year").reset_index(drop=True)



def save_plots(df: pd.DataFrame) -> None:
    if plt is None:
        print("\nPlot generation skipped: matplotlib is not installed.")
        return

    os.makedirs("plots", exist_ok=True)

    plt.figure(figsize=(8, 5))
    plt.plot(df["year"], df["water_consumption_billion_gallons"], marker="o")
    plt.title("Water Use Over Time")
    plt.xlabel("Year")
    plt.ylabel("Billion Gallons")
    plt.savefig("plots/q1_line.png")
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.bar(df["year"], df["replenishment_percent"])
    plt.title("Water Replenishment Percentage Over Time")
    plt.xlabel("Year")
    plt.ylabel("Replenishment (%)")
    plt.savefig("plots/q2_bar.png")
    plt.close()

    corr = df[["water_consumption_billion_gallons", "replenishment_percent"]].corr()

    plt.figure(figsize=(6, 5))
    plt.imshow(corr, cmap="coolwarm", interpolation="none")
    plt.colorbar()
    plt.xticks([0, 1], corr.columns)
    plt.yticks([0, 1], corr.columns)
    plt.title("Correlation Matrix")
    plt.savefig("plots/correlation_matrix.png")
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.scatter(df["water_consumption_billion_gallons"], df["replenishment_percent"])
    plt.title("Water Consumption vs Replenishment Percentage")
    plt.xlabel("Water Consumption (Billions of Gallons)")
    plt.ylabel("Replenishment (%)")
    plt.savefig("plots/Consumption_VS_Replenishment_Percentage.png")
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.plot(df["year"], df["water_consumption_billion_gallons"], label="Water Consumption")
    plt.plot(df["year"], df["replenishment_percent"], label="Replenishment %")
    plt.title("Water Consumption vs Replenishment Over Time")
    plt.xlabel("Year")
    plt.ylabel("Water Consumption (Billions) & Replenishment (%)")
    plt.legend(loc="upper left")
    plt.savefig("plots/Consumption_VS_Replenishment_Time.png")
    plt.close()



def main() -> None:
    df = load_water_usage_data()

    print("Shape:", df.shape)
    print("\nDtypes:\n", df.dtypes)
    print("\nHead:\n", df.head().to_string(index=False))
    print("\nMissing values:\n", df.isna().sum())
    print("\nDescribe:\n", df.describe())

    print("\nQuestions:")
    print("1. How does water use change over time?")
    print("2. Has replenishment percentage increased over time?")
    print("3. Is there a relationship between water consumption and replenishment percentage?")
    print("4. How do water consumption and replenishment percentage compare over time?")

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
    print("\nCorrelation matrix:\n", corr)

    save_plots(df)
    run_predictive_analysis(df)

def run_predictive_analysis(df: pd.DataFrame) -> None:
    try:
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LinearRegression, Ridge
        from sklearn.metrics import mean_squared_error
        import numpy as np
    except ModuleNotFoundError:
        print("\nPredictive analysis skipped: scikit-learn is not installed.")
        return

    print("\nPredictive Analysis Questions:")
    print("1. Can water consumption predict replenishment percentage?")
    print("2. How does Ridge regularization affect model performance?")

    model_df = df.dropna(
        subset=["water_consumption_billion_gallons", "replenishment_percent"]
    )

    X = model_df[["water_consumption_billion_gallons"]]
    y = model_df["replenishment_percent"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # Linear Regression
    reg = LinearRegression()
    reg.fit(X_train, y_train)
    y_pred = reg.predict(X_test)

    r2 = reg.score(X_test, y_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print("\nLinear Regression Results:")
    print("R² Score:", r2)
    print("RMSE:", rmse)

    # Ridge Regression
    alphas = [0.1, 1.0, 10.0, 100.0]
    ridge_scores = []

    for alpha in alphas:
        ridge = Ridge(alpha=alpha)
        ridge.fit(X_train, y_train)
        ridge_scores.append(ridge.score(X_test, y_test))

    print("\nRidge Regression Scores:")
    for alpha, score in zip(alphas, ridge_scores):
        print(f"Alpha {alpha}: {score}")

    if plt is not None:
        os.makedirs("plots", exist_ok=True)

        # Regression line plot
        plt.figure(figsize=(8, 5))
        plt.scatter(X, y, label="Actual Data")
        plt.plot(X, reg.predict(X), color="red", label="Linear Regression")
        plt.title("Predicting Replenishment from Water Consumption")
        plt.xlabel("Water Consumption (Billion Gallons)")
        plt.ylabel("Replenishment (%)")
        plt.legend()
        plt.savefig("plots/regression_plot.png")
        plt.close()

        # Ridge performance plot
        plt.figure(figsize=(8, 5))
        plt.plot(alphas, ridge_scores, marker="o")
        plt.title("Ridge Regression Performance")
        plt.xlabel("Alpha Regularization Strength")
        plt.ylabel("R² Score")
        plt.savefig("plots/regression_performance_plot.png")
        plt.close()

    print("\nPredictive Analysis Summary:")
    print(
        "- Linear regression was used to test whether water consumption could predict "
        "replenishment percentage."
    )
    print(
        "- Ridge regression was used to evaluate how regularization affects model performance."
    )
    print(
        "- Because the dataset is small, results should be interpreted cautiously."
    )

if __name__ == "__main__":
    main()
