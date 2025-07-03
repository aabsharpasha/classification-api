import torch
from sentence_transformers import SentenceTransformer, CrossEncoder, util

# Models
_be = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")   # parrot check
_ce = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")            # similarity

# Hyper‑parameters
PARROT = 0.80       # answer ≈ question  →  No Match
TEMP   = 8.0        # higher = sharper confidences (try 6‑10)
MIN_CONF = 0.40     # if best soft‑max prob < 40 %  →  No Match

def classify(criteria: dict, answer: str, question: str):
    labels, crit_sentences = zip(*criteria.items())

    # 1️⃣  Parrot guard
    if util.cos_sim(
        _be.encode(answer, convert_to_tensor=True),
        _be.encode(question, convert_to_tensor=True)
    ).item() >= PARROT:
        return "No Match", 100.0

    # 2️⃣  Cross‑encoder scores
    pairs  = [(answer, crit) for crit in crit_sentences]
    logits = torch.tensor(_ce.predict(pairs))                 # shape [n_criteria]

    # 3️⃣  Temperature‑scaled soft‑max  →  probabilities
    probs     = torch.softmax(logits * TEMP, dim=0)
    best_idx  = int(torch.argmax(probs))
    best_prob = float(probs[best_idx])

    # 4️⃣  Decide label
    if best_prob < MIN_CONF:
        # Everything scored low → treat as No Match
        return "No Match", 100.0

    # Otherwise accept the best label (even if answer goes beyond Gold wording)
    return labels[best_idx], round(best_prob * 100, 2)
