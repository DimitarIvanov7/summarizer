from fastapi import FastAPI, Request
from pydantic import BaseModel
from Summarizer import textrank_summary_bg, lsa_summary_bg
from TextPreprocessing import clean_sentence
from fastapi.middleware.cors import CORSMiddleware
from Evaluation import evaluate_summary

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SummarizeRequest(BaseModel):
    text: str
    method: str = "textrank"
    n_sentences: int = 3

@app.post("/summarize")
async def summarize(req: SummarizeRequest):
    if req.method == "lsa":
        summary = lsa_summary_bg(req.text, clean_fn=clean_sentence, n_sentences=req.n_sentences, k_topics=3)
    else:
        summary = textrank_summary_bg(req.text, clean_fn=clean_sentence, n_sentences=req.n_sentences)
    
    scores = evaluate_summary(req.text, summary)
    # Format scores for JSON response
    eval_result = {
        metric: {
            "precision": scores[metric][0],
            "recall": scores[metric][1],
            "f_measure": scores[metric][2]
        }
        for metric in scores
    }
    return {
        "summary": summary,
        "evaluation": eval_result
    }