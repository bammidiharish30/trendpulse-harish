import requests

#Make the API Calls

url = "https://hacker-news.firebaseio.com/v0/topstories.json"
headers = {"User-Agent": "TrendPulse/1.0"}

response = requests.get(url, headers=headers)
story_ids = response.json()

story_ids = response.json()[:500]
print(story_ids)

print(len(story_ids))  # should print 500

#first 500 stories
import requests

headers = {"User-Agent": "TrendPulse/1.0"}

for story_id in story_ids[:500]:
    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"

    try:
        response = requests.get(url, headers=headers)
        story = response.json()

        if story and "title" in story:
            print(story["title"])

    except Exception:
        print(f"Error fetching story {story_id}")

#Divided by categories
import requests
import time
from datetime import datetime

# -----------------------------
# CATEGORY KEYWORDS
# -----------------------------
CATEGORY_KEYWORDS = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# -----------------------------
# STORAGE
# -----------------------------
categories = {
    "technology": [],
    "worldnews": [],
    "sports": [],
    "science": [],
    "entertainment": []
}

filled = set()

# -----------------------------
# FETCH SINGLE STORY
# -----------------------------
def get_story(story_id):
    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

# -----------------------------
# CATEGORY DETECTION
# -----------------------------
def get_category(title):
    title = title.lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in title:
                return category
    return None

# -----------------------------
# GET TOP STORY IDS
# -----------------------------
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
response = requests.get(url)
story_ids = response.json()[:500]   # first 500 only

# -----------------------------
# MAIN LOOP
# -----------------------------
for story_id in story_ids:

    story = get_story(story_id)

    if not story or "title" not in story:
        continue

    category = get_category(story["title"])

    if category is None:
        continue

    # limit per category
    if len(categories[category]) >= 25:
        continue

    #Extract the Fields
    
    data = {
        "post_id": story.get("id"),
        "title": story.get("title"),
        "category": category,
        "score": story.get("score"),
        "num_comments": story.get("descendants"),
        "author": story.get("by"),
        "collected_at": datetime.now().isoformat()
    }

    categories[category].append(data)

    # -----------------------------
    # sleep when category completes
    # -----------------------------
    if len(categories[category]) == 25 and category not in filled:
        print(f"{category} completed")
        filled.add(category)
        time.sleep(2)

    # stop early when all full
    if all(len(v) >= 25 for v in categories.values()):
        break

# -----------------------------
# FINAL OUTPUT
# -----------------------------
total = 0

for cat, items in categories.items():
    print(f"\n{cat.upper()} ({len(items)} posts)")
    for item in items:
        print("-", item["title"])
    total += len(items)

from datetime import datetime

# assume categories, get_story, get_category already exist

for story_id in story_ids:  # ✅ LOOP is REQUIRED

    story = get_story(story_id)

    if not story or "title" not in story:
        continue

    # STEP 1: categorize
    category = get_category(story["title"])

    if category is None:
        continue

    # STEP 2: extract fields
    data = {
        "post_id": story.get("id"),
        "title": story.get("title"),
        "category": category,
        "score": story.get("score"),
        "num_comments": story.get("descendants"),
        "author": story.get("by"),
        "collected_at": datetime.now().isoformat()
    }


    # store result
    categories[category].append(data)

#Save to a JSON File

import os
import json
from datetime import datetime


# CREATE DATA FOLDER

if not os.path.exists("data"):
    os.makedirs("data")


# FILE NAME WITH DATE

date_str = datetime.now().strftime("%Y%m%d")
file_path = f"data/trends_{date_str}.json"

# SAVE DATA

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(final_stories, f, indent=4)


# FINAL OUTPUT
print("In first 500 stories we have only 90 stories belongs to the respective categories")
print(f"Collected {len(final_stories)} stories. Saved to {file_path}")


