import torch
from sentence_transformers import SentenceTransformer, util

_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def classify(criteria: dict, answer: str):
    """Return (chosen_label, confidence 0‑1)"""
    labels, sentences = zip(*criteria.items())
    embeddings = _model.encode(
        [answer, *sentences],
        convert_to_tensor=True,
        normalize_embeddings=True
    )
    ans_emb, crit_embs = embeddings[0], embeddings[1:]
    sims = util.cos_sim(ans_emb, crit_embs).squeeze(0)   # vector
    best = int(torch.argmax(sims))
    return labels[best], round(float(sims[best]), 1)
