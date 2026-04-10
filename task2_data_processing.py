
import pandas as pd
import os
from datetime import datetime

# ---------------------------------------------
# STEP 1: LOAD JSON FILE
# ---------------------------------------------

# Get today's date to match Task 1 file
date_str = datetime.now().strftime("%Y%m%d")
file_path = f"data/trends_{date_str}.json"

# Check if file exists
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    exit()

# Load JSON into DataFrame
df = pd.read_json(file_path)

print(f"Loaded {len(df)} stories from {file_path}")


# ---------------------------------------------
# STEP 2: CLEAN THE DATA
# ---------------------------------------------

# 1. Remove duplicates based on post_id
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# 2. Remove rows with missing important values
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# 3. Convert data types to correct format
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].fillna(0).astype(int)

# 4. Remove low-quality stories (score < 5)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# 5. Remove extra whitespace from title
df["title"] = df["title"].str.strip()


# ---------------------------------------------
# STEP 3: SAVE CLEANED DATA AS CSV
# ---------------------------------------------

# Ensure data folder exists
if not os.path.exists("data"):
    os.makedirs("data")

output_path = "data/trends_clean.csv"

# Save to CSV
df.to_csv(output_path, index=False)

print(f"
Saved {len(df)} rows to {output_path}")


# ---------------------------------------------
# STEP 4: PRINT SUMMARY (STORIES PER CATEGORY)
# ---------------------------------------------

print("
Stories per category:")
category_counts = df["category"].value_counts()

for category, count in category_counts.items():
    print(f"  {category:<15} {count}")


