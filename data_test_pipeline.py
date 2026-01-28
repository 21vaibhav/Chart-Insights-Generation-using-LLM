import pandas as pd
from pipelines.data_pipeline import run_data_pipeline

# Load sample data
df = pd.read_csv(r"D:\DAIAugust2025\Python\Anurag\cdac_project\input\data\raw_files\20260124_191629_tips (1).csv")

processed_df, schema, summary = run_data_pipeline(
    df,
    drop_duplicates=True,
    drop_nulls=False,
    fill_missing=True,
)

print("\n=== PROCESSED DF ===")
print(processed_df.head())

print("\n=== SCHEMA INFO ===")
print(schema)

print("\n=== SUMMARY ===")
print(summary)
