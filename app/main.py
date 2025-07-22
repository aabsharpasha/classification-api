

from fastapi import FastAPI
from .schemas import RequestBody, ResponseBody, ItemOut
from .logic import classify_response

app = FastAPI(title="Classifier API")

@app.post("/categorize", response_model=ResponseBody)
def categorize(body: RequestBody):
    results = [
        ItemOut(
            id=item.id,
            question=item.question,
            response=item.answer,
            picked_category=label,
            confidence=conf
        )
        for item in body.items
        for label, conf in [classify_response(item.criteria, item.answer, item.question)]
    ]
    return ResponseBody(results=results)
