import pandas as pd
import os

DATA_FILE = "data/diseases.csv"
os.makedirs("data", exist_ok=True)

def load_diseases_df():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["id","title","summary","overview","symptoms","prevention","image"])
        df.to_csv(DATA_FILE, index=False)
        return df
    df = pd.read_csv(DATA_FILE, dtype=str)
    if "id" in df.columns:
        df["id"] = pd.to_numeric(df["id"], errors="coerce").fillna(0).astype(int)
    return df

def save_diseases_df(df):
    df.to_csv(DATA_FILE, index=False)

def get_next_id(df):
    if df.empty:
        return 1
    return int(df["id"].max()) + 1
