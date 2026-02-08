import json
import random
from Summarizer import textrank_summary_bg, lsa_summary_bg
from TextPreprocessing import clean_sentence
from pathlib import Path

def load_jsonl(path):
    items = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items

def pick_article(items, title_contains=None):
    if title_contains:
        filtered = [it for it in items if title_contains.lower() in it["title"].lower()]
        return random.choice(filtered) if filtered else None
    return random.choice(items)


from pathlib import Path

DATASET_PATH = Path(__file__).resolve().parent / "dataset_bg_wiki_informatics_100.jsonl"

def main():
    items = load_jsonl(DATASET_PATH)

    print("\n=== BG WIKI SUMMARIZER (TextRank / LSA) ===")
    print(f"Loaded articles: {len(items)}")

    query = input("\nSearch in title (optional, press Enter to skip): ").strip()
    article = pick_article(items, title_contains=query) if query else pick_article(items)

    if not article:
        print("No matching articles found.")
        return

    print("\n--- ARTICLE ---")
    print("Title:", article["title"])
    print("URL:", article.get("url", ""))

    print("\nChoose summarization method:")
    print("1 - TextRank")
    print("2 - LSA")
    method = input("\nEnter 1 or 2: ").strip()

    n = input("\nHow many sentences should the summary contain? (default = 3): ").strip()
    n = int(n) if n else 3

    text = article["text"]

    print("\n=== GENERATED SUMMARY ===\n")
    if method == "1":
        summary = textrank_summary_bg(text, clean_fn=clean_sentence, n_sentences=n)
    elif method == "2":
        summary = lsa_summary_bg(text, clean_fn=clean_sentence, n_sentences=n, k_topics=3)
    else:
        print("Invalid choice.")
        return

    print(summary)

if __name__ == "__main__":
    main()