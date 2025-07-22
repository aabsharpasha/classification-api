from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import re
import os

# Load HuggingFace token from environment variable for better security
load_dotenv()  # Automatically reads .env file
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HuggingFace token not found. Please set the HF_TOKEN environment variable.")

# Initialize HuggingFace Inference Client
client = InferenceClient(
    model="deepseek-ai/DeepSeek-V3",
    token=HF_TOKEN
)

def classify_response(criteria, answer, question):
    prompt = f"""You are a financial audit compliance evaluator.

Your task is to evaluate the following response based on the provided rubric and classify it into one of the following categories:

- Broken
- Needs Improvement
- Ideal
- Gold Standard
- No Match

### Instructions:
- If the response is better than Gold Standard, classify it as Gold Standard.
- If the response is worse than Broken, classify it as Broken.
- If the response is not relevant to the rubric, classify it as No Match.
- Only respond with one of the categories above, nothing else.
- Use No Match if the response is completely unrelated to the rubric.
- Also return your confidence score as a number from 0 to 100, where 100 means highest confidence.

### Rubric:
{criteria}

### Response:
{answer}

### Classification (Format: Label, Confidence):"""

    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=20,
            temperature=0.3,
        )
        raw_output = completion.choices[0].message.content.strip()
        print("Raw output:", raw_output)

        # Try to extract using regex
        match = re.match(r"(?i)(broken|needs improvement|ideal|gold standard|no match)[^\d]*(\d{1,3})", raw_output)
        if match:
            label = match.group(1).title()
            confidence = float(match.group(2))
            confidence = min(confidence, 100.0)
            return label, confidence

        print("Unrecognized format, fallback:", raw_output)
        return "Broken", 0.0

    except Exception as err:
        print(f"Client Error: {err}")
        return "Broken", 0.0
