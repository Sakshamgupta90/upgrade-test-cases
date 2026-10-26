import pandas as pd

SALES = [
    {"region": "North", "product": "Widget", "units": 12, "price": 2.5},
    {"region": "South", "product": "Gadget", "units": 7, "price": 4.0},
    {"region": "North", "product": "Gadget", "units": 3, "price": 4.0},
    {"region": "East", "product": "Widget", "units": 9, "price": 2.5},
]


def build_report(rows):
    df = pd.DataFrame([rows[0]])
    for row in rows[1:]:
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df["revenue"] = df["units"] * df["price"]
    return df


def summary_by_region(df):
    return df.groupby("region").mean(numeric_only=True)


def column_types(df):
    return {name: str(col.dtype) for name, col in df.items()}


def save(df, path):
    df.to_csv(path, index=False, lineterminator="\n")


if __name__ == "__main__":
    report = build_report(SALES)
    print(summary_by_region(report))
    print(column_types(report))
    save(report, "report.csv")
