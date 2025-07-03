import torch
from sentence_transformers import SentenceTransformer, CrossEncoder, util

# Load models
_be = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")                  # for parrot check
_ce = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")                           # for actual classification

# Hyperparameters
PARROT = 0.8   # Similarity threshold: answer ≈ question → "No Match"
TEMP   = 5.0   # Scaling for sharper softmax confidence (tune 3–8)

def classify(criteria: dict, answer: str, question: str):
    labels, crit_sentences = zip(*criteria.items())

    # 1. Parrot guard — don't accept answers that repeat the question
    if util.cos_sim(
        _be.encode(answer, convert_to_tensor=True),
        _be.encode(question, convert_to_tensor=True)
    ).item() >= PARROT:
        return "No Match", 100

    # 2. Build (answer, criterion) pairs
    pairs = [(answer, crit) for crit in crit_sentences]

    # 3. Get logits from cross-encoder
    logits = torch.tensor(_ce.predict(pairs))  # shape: [n_criteria]

    # 4. Apply temperature-scaled softmax
    probs = torch.softmax(logits * TEMP, dim=0)
    best_idx = int(torch.argmax(probs))

    return labels[best_idx], round(float(probs[best_idx])*100, 2)
