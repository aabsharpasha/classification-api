# Classification API

A FastAPI-based classification service that categorizes responses using AI models.

## Features

- FastAPI-based REST API
- AI-powered classification using Groq API
- Docker containerization
- Health checks
- Environment-based configuration

## Prerequisites

- Docker and Docker Compose
- Groq API token
- HuggingFace API token (optional, currently using Groq)

## Quick Start

1. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit .env file with your API tokens:**
   ```bash
   HF_TOKEN=your_huggingface_token_here
   GROQ_API_KEY=your_groq_token_here
   ```

3. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

4. **Access the API:**
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/docs

## Manual Docker Build

1. **Build the image:**
   ```bash
   docker build -t classification-api .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8000:8000 \
     -e HF_TOKEN=your_token \
     -e GROQ_API_KEY=your_token \
     classification-api
   ```

## API Usage

### Endpoint: POST /categorize

**Request Body:**
```json
{
  "items": [
    {
      "id": 1,
      "question": "How do you handle audit findings?",
      "criteria": {
        "Broken": "No process",
        "Needs Improvement": "Basic process",
        "Ideal": "Good process",
        "Gold Standard": "Excellent process"
      },
      "answer": "We have a comprehensive audit tracking system"
    }
  ]
}
```

**Response:**
```json
{
  "results": [
    {
      "id": 1,
      "question": "How do you handle audit findings?",
      "response": "We have a comprehensive audit tracking system",
      "picked_category": "Ideal",
      "confidence": 85.0
    }
  ]
}
```

## Environment Variables

- `HF_TOKEN`: HuggingFace API token (required)
- `GROQ_API_KEY`: Groq API token (required)
- `PORT`: Port to run the API on (default: 8000)

## Development

To run locally without Docker:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables:**
   ```bash
   export HF_TOKEN=your_token
   export GROQ_API_KEY=your_token
   ```

3. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

## Health Check

The container includes a health check that verifies the API is responding:
- Endpoint: `GET /docs`
- Interval: 30 seconds
- Timeout: 10 seconds
- Retries: 3
- Start period: 40 seconds

