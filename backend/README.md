# MTG AI Search Backend

FastAPI backend service for MTG AI Search, providing natural language card search capabilities.

## Features

- Natural language card search using AI
- Integration with Scryfall API
- Support for multiple AI providers (OpenAI, AIHubMix)
- RESTful API endpoints

## Setup

1. Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
cp env_example.txt .env
# Edit .env with your API keys
```

4. Run the development server:

```bash
uvicorn app.main:app --reload
```

## API Endpoints

- `POST /api/search`: Search cards using natural language
- `POST /api/validate-key`: Validate API keys
- `POST /api/models`: Get available AI models
- `GET /api/health`: Health check endpoint

## Deployment

This service is deployed on Render.com. The deployment configuration is in `render.yaml`.

