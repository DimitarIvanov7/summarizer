import requests
import time
import json
from collections import deque

API = "https://bg.wikipedia.org/w/api.php"

HEADERS = {
    "User-Agent": "SummarizerCourseProject/1.0 (contact: student@example.com)"
}

def categorymembers_request(cmtitle, cmnamespace, cmlimit=50, cmcontinue=None):

    params = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "cmtitle": cmtitle,
        "cmnamespace": cmnamespace,
        "cmlimit": cmlimit
    }
    if cmcontinue:
        params["cmcontinue"] = cmcontinue

    r = requests.get(API, params=params, headers=HEADERS, timeout=30)
    r.raise_for_status()
    data = r.json()

    members = data.get("query", {}).get("categorymembers", [])
    next_continue = data.get("continue", {}).get("cmcontinue")

    return members, next_continue


def get_all_page_titles_in_category(category_title, sleep_s=0.2):
    titles = []
    cmcontinue = None
    while True:
        members, cmcontinue = categorymembers_request(
            cmtitle=category_title,
            cmnamespace=0,
            cmlimit=50,
            cmcontinue=cmcontinue
        )
        titles.extend([m["title"] for m in members])
        if not cmcontinue:
            break
        time.sleep(sleep_s)
    return titles


def get_all_subcategory_titles(category_title, sleep_s=0.2):
    subcats = []
    cmcontinue = None
    while True:
        members, cmcontinue = categorymembers_request(
            cmtitle=category_title,
            cmnamespace=14,
            cmlimit=50,
            cmcontinue=cmcontinue
        )
        subcats.extend([m["title"] for m in members])
        if not cmcontinue:
            break
        time.sleep(sleep_s)
    return subcats


def bfs_collect_titles_from_category_tree(
    root_category="Информатика",
    target_titles=300,
    max_categories=500,
    sleep_s=0.2
):
    root = f"Категория:{root_category}"

    q = deque([root])
    visited_cats = set([root])

    titles = []
    seen_titles = set()

    while q and len(titles) < target_titles and len(visited_cats) < max_categories:
        cat = q.popleft()

        # 1) collect pages from this category
        page_titles = get_all_page_titles_in_category(cat, sleep_s=sleep_s)
        for t in page_titles:
            if t not in seen_titles:
                seen_titles.add(t)
                titles.append(t)
                if len(titles) >= target_titles:
                    break

        # 2) enqueue subcategories
        subcats = get_all_subcategory_titles(cat, sleep_s=sleep_s)
        for sc in subcats:
            if sc not in visited_cats:
                visited_cats.add(sc)
                q.append(sc)

        time.sleep(sleep_s)

    return titles


def get_plaintext_extract(title):
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts|info",
        "inprop": "url",
        "explaintext": 1,
        "exsectionformat": "plain",
        "redirects": 1,
        "titles": title
    }
    r = requests.get(API, params=params, headers=HEADERS, timeout=30)
    r.raise_for_status()
    data = r.json()

    pages = data.get("query", {}).get("pages", {})
    if not pages:
        return None

    page = next(iter(pages.values()))
    if page.get("missing") is not None:
        return None

    extract = (page.get("extract") or "").strip()
    fullurl = page.get("fullurl")

    if len(extract) < 1200:
        return None

    return extract, fullurl

def build_dataset_from_category_bfs(
    category="Информатика",
    target=100,
    out_path="dataset_bg_wiki_informatics_100.jsonl"
):
    items = []

    candidate_titles = bfs_collect_titles_from_category_tree(
        root_category=category,
        target_titles=max(target * 5, 300),  # generous pool
        max_categories=800,
        sleep_s=0.2
    )


    seen = set()
    for title in candidate_titles:
        if len(items) >= target:
            break
        if title in seen:
            continue
        seen.add(title)

        res = get_plaintext_extract(title)
        if not res:
            continue

        extract, url = res
        rest_text = extract

        items.append({
            "title": title,
            "url": url,
            "text": rest_text
        })

        print(f"[{len(items)}/{target}] {title}")
        time.sleep(0.3)

    with open(out_path, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")

    print(f"Saved: {out_path}")


if __name__ == "__main__":
    build_dataset_from_category_bfs()
