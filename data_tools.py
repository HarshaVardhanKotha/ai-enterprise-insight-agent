import pandas as pd

DATA_PATH = "data/business_metrics.csv"

def load_metrics():
    return pd.read_csv(DATA_PATH)

def summarize_metrics():
    df = load_metrics()

    total_sales = df["sales_usd"].sum()
    avg_satisfaction = df["customer_satisfaction"].mean()
    total_tickets = df["support_tickets"].sum()

    lowest_satisfaction_region = df.sort_values("customer_satisfaction").iloc[0]["region"]
    highest_sales_region = df.sort_values("sales_usd", ascending=False).iloc[0]["region"]

    return {
        "total_sales_usd": int(total_sales),
        "average_customer_satisfaction": round(float(avg_satisfaction), 2),
        "total_support_tickets": int(total_tickets),
        "lowest_satisfaction_region": lowest_satisfaction_region,
        "highest_sales_region": highest_sales_region
    }

def region_report(region: str):
    df = load_metrics()
    region_data = df[df["region"].str.lower() == region.lower()]

    if region_data.empty:
        return {"error": f"No data found for region: {region}"}

    row = region_data.iloc[0]
    return {
        "region": row["region"],
        "sales_usd": int(row["sales_usd"]),
        "support_tickets": int(row["support_tickets"]),
        "customer_satisfaction": float(row["customer_satisfaction"]),
        "return_rate_percent": float(row["return_rate_percent"])
    }
