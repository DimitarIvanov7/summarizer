import json
import random
from pathlib import Path
from Evaluation import evaluate_summary
from main import load_jsonl
from Summarizer import textrank_summary_bg, lsa_summary_bg
from TextPreprocessing import clean_sentence

DATASET_PATH = Path(__file__).resolve().parent / "dataset_bg_wiki_informatics_100.jsonl"

def evaluate_all(articles, summarization_method):

    totalScores = {
        "rouge1": {"precision": 0, "recall": 0, "fmeasure": 0},
        "rouge2": {"precision": 0, "recall": 0, "fmeasure": 0},
        "rougeL": {"precision": 0, "recall": 0, "fmeasure": 0},
    }


    for a in articles:
        text = a["text"]

        if summarization_method == "TextRank":
            summary = textrank_summary_bg(text, clean_fn=clean_sentence, n_sentences=5)
        elif summarization_method == "LSA":
            summary = lsa_summary_bg(text, clean_fn=clean_sentence, n_sentences=5, k_topics=3)
        else:
            print("Invalid Method")
            return

        scores = evaluate_summary(text, summary)

        for s in scores:
            precision = scores[s][0]
            recall = scores[s][1]
            fmeasure = scores[s][2]

            totalScores[s]["precision"] += precision
            totalScores[s]["recall"] += recall
            totalScores[s]["fmeasure"] += fmeasure

    avgTotal = average_scores(totalScores, len(articles))
    return avgTotal


def average_scores(scores, iterations):
    """
    Compute the average of nested ROUGE score dictionaries.

    iterations: number of updates accumulated
    """
    if iterations == 0:
        raise ValueError("iterations must be > 0")

    return {
        metric: {k: v / iterations for k, v in inner.items()}
        for metric, inner in scores.items()
    }


def main():
    all_articles = load_jsonl(DATASET_PATH)

    avgTextRank = evaluate_all(all_articles, "TextRank")
    avgLSA = evaluate_all(all_articles, "TextRank")

    print("========== Average Scores ==========\n")

    print("########## TextRank ##########\n")
    for s in avgTextRank:
        print("==========", s ,"==========")
        print("Precision: ", avgTextRank[s]["precision"])
        print("Recall: ", avgTextRank[s]["recall"])
        print("F-measure: ", avgTextRank[s]["fmeasure"])
        print()

    print()
    print("\n########## LSA ##########\n")
    for s in avgLSA:
        print("==========", s, "==========")
        print("Precision: ", avgLSA[s]["precision"])
        print("Recall: ", avgLSA[s]["recall"])
        print("F-measure: ", avgLSA[s]["fmeasure"])
        print()



if __name__ == "__main__":
    main()