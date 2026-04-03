import pandas as pd
from pathlib import Path
from database import CSV_PATH

def add_is_custom_column():

    csv_path = Path(CSV_PATH)

    df = pd.read_csv(csv_path)

    # Add column only if it doesn't exist
    if "is_custom" not in df.columns:
        df["is_custom"] = 0

    # Save back to same file
    df.to_csv(csv_path, index=False)

    print(f"Updated CSV: {csv_path}")



if __name__ == "__main__":
    add_is_custom_column()