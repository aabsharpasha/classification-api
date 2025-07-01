from fastapi import FastAPI
from .schemas import RequestBody, ResponseBody, ItemOut
from .logic import classify

app = FastAPI(title="Classifier API")

@app.post("/categorize", response_model=ResponseBody)
def categorize(body: RequestBody):
    results = [
        ItemOut(
            id=item.id,
            question=item.question,
            picked_category=label,
            confidence=conf
        )
        for item in body.items
        for label, conf in [classify(item.criteria, item.answer)]
    ]
    return ResponseBody(results=results)
