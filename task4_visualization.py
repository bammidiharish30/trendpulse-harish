import pandas as pd
import matplotlib.pyplot as plt
import os

# -----------------------------
# 1. LOAD DATA
# -----------------------------
df = pd.read_csv("data/trends_analysed.csv")

print("Data loaded:", df.shape)

# -----------------------------
# 2. CREATE OUTPUT FOLDER
# -----------------------------
os.makedirs("outputs", exist_ok=True)

# -----------------------------
# 3. CHART 1: TOP 10 STORIES BY SCORE
# -----------------------------
top10 = df.sort_values(by="score", ascending=False).head(10)

# shorten titles
top10["short_title"] = top10["title"].apply(lambda x: x[:50])

plt.figure(figsize=(10, 6))
plt.barh(top10["short_title"], top10["score"])
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")
plt.gca().invert_yaxis()

plt.savefig("outputs/chart1_top_stories.png")
plt.show()

# -----------------------------
# 4. CHART 2: STORIES PER CATEGORY
# -----------------------------
category_counts = df["category"].value_counts()

plt.figure(figsize=(8, 5))
plt.bar(category_counts.index, category_counts.values)
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")

plt.savefig("outputs/chart2_categories.png")
plt.show()

# -----------------------------
# 5. CHART 3: SCORE VS COMMENTS (SCATTER)
# -----------------------------
plt.figure(figsize=(8, 6))

popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.scatter(popular["score"], popular["num_comments"], label="Popular", alpha=0.7)
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular", alpha=0.7)

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()

plt.savefig("outputs/chart3_scatter.png")
plt.show()

# -----------------------------
# 6. BONUS: DASHBOARD (2x2 GRID)
# -----------------------------
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("TrendPulse Dashboard")

# Chart 1
axs[0, 0].barh(top10["short_title"], top10["score"])
axs[0, 0].set_title("Top 10 Stories")
axs[0, 0].invert_yaxis()

# Chart 2
axs[0, 1].bar(category_counts.index, category_counts.values)
axs[0, 1].set_title("Category Count")

# Chart 3
axs[1, 0].scatter(popular["score"], popular["num_comments"], label="Popular")
axs[1, 0].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
axs[1, 0].set_title("Score vs Comments")
axs[1, 0].legend()

# empty plot (optional)
axs[1, 1].axis("off")

plt.tight_layout()
plt.savefig("outputs/dashboard.png")
plt.show()

print("All charts saved in outputs/ folder")
