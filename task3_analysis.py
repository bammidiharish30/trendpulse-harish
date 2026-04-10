import pandas as pd
import numpy as np

# -----------------------
# 1. LOAD DATA
# -----------------------
df = pd.read_csv("data/trends_clean.csv")

print("Loaded data:", df.shape)

print("\nFirst 5 rows:")
print(df.head())

print("\nAverage score:", df["score"].mean())
print("Average comments:", df["num_comments"].mean())

# -----------------------
# 2. NUMPY ANALYSIS
# -----------------------
scores = df["score"].to_numpy()

print("\n--- NumPy Stats ---")
print("Mean score:", np.mean(scores))
print("Median score:", np.median(scores))
print("Std deviation:", np.std(scores))
print("Max score:", np.max(scores))
print("Min score:", np.min(scores))

# Most stories per category
print("\nMost stories in category:")
print(df["category"].value_counts().idxmax())

# Most commented story
top_story = df.loc[df["num_comments"].idxmax()]
print("\nMost commented story:")
print(top_story["title"], "-", top_story["num_comments"])

# -----------------------
# 3. NEW COLUMNS
# -----------------------

df["engagement"] = df["num_comments"] / (df["score"] + 1)

avg_score = df["score"].mean()
df["is_popular"] = df["score"] > avg_score

# -----------------------
# 4. SAVE OUTPUT
# -----------------------
output_path = "data/trends_analysed.csv"
df.to_csv(output_path, index=False)

print("\nSaved to", output_path)

