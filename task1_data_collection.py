import requests
import time
import os
import json
from datetime import datetime

# ---------------------------------------------
# CONFIGURATION
# ---------------------------------------------

HEADERS = {"User-Agent": "TrendPulse/1.0"}

TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Category keywords (case-insensitive)
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

MAX_PER_CATEGORY = 25


# ---------------------------------------------
# FUNCTION: FETCH TOP STORY IDS
# ---------------------------------------------
def fetch_top_story_ids(limit=500):
    try:
        response = requests.get(TOP_STORIES_URL, headers=HEADERS)
        response.raise_for_status()
        return response.json()[:limit]
    except Exception as e:
        print(f"Error fetching top stories: {e}")
        return []


# ---------------------------------------------
# FUNCTION: FETCH SINGLE STORY
# ---------------------------------------------
def fetch_story(story_id):
    try:
        response = requests.get(ITEM_URL.format(story_id), headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching story {story_id}: {e}")
        return None


# ---------------------------------------------
# FUNCTION: ASSIGN CATEGORY
# ---------------------------------------------
def get_category(title):
    title_lower = title.lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category

    return None


# ---------------------------------------------
# MAIN SCRIPT
# ---------------------------------------------
def main():
    top_ids = fetch_top_story_ids()

    # Storage for categorized stories
    categorized_data = {cat: [] for cat in CATEGORIES.keys()}

    for story_id in top_ids:
        story = fetch_story(story_id)

        if not story or "title" not in story:
            continue

        category = get_category(story["title"])

        if category and len(categorized_data[category]) < MAX_PER_CATEGORY:
            # Extract required fields
            data = {
                "post_id": story.get("id"),
                "title": story.get("title"),
                "category": category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by", "unknown"),
                "collected_at": datetime.now().isoformat()
            }

            categorized_data[category].append(data)

        # Stop if all categories are filled
        if all(len(categorized_data[cat]) >= MAX_PER_CATEGORY for cat in CATEGORIES):
            break

    # ---------------------------------------------
    # APPLY 2-SECOND DELAY PER CATEGORY (REQUIREMENT)
    # ---------------------------------------------
    for category in categorized_data:
        time.sleep(2)

    # Combine all categories into one list
    final_data = []
    for cat in categorized_data:
        final_data.extend(categorized_data[cat])

    # ---------------------------------------------
    # SAVE TO JSON FILE
    # ---------------------------------------------
    if not os.path.exists("data"):
        os.makedirs("data")

    date_str = datetime.now().strftime("%Y%m%d")
    file_path = f"data/trends_{date_str}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=4)

    # ---------------------------------------------
    # OUTPUT
    # ---------------------------------------------
    print(f"Collected {len(final_data)} stories. Saved to {file_path}")


# ---------------------------------------------
# RUN SCRIPT
# ---------------------------------------------
if __name__ == "__main__":
    main()
