# Development Notes for AI Assistants

## Project Overview

This is a Magic: The Gathering (MTG) AI-powered card search application with a React frontend and FastAPI backend.

## Remote Deployment URLs

- **Frontend**: https://mtg-ai-frontend.onrender.com
- **Backend**: https://mtg-ai-backend.onrender.com

## Project Structure

```
demo/
├── mtg-ai-frontend/     # React + TypeScript + Vite frontend
└── mtg-ai-backend/      # Python FastAPI backend
```

## Key Technologies

- **Frontend**: React, TypeScript, Vite, Tailwind CSS, Axios
- **Backend**: Python, FastAPI, httpx, pydantic
- **Deployment**: Render.com
- **Version Control**: Git, GitHub

## Important Configuration

### Encryption

- Uses simple Base64 + XOR masking for API key protection
- Key: `"mtg2024"`
- Implemented in both frontend and backend
- Middleware handles encryption/decryption automatically

### API Endpoints

- `POST /api/search` - Main search endpoint
- `GET /api/models` - Get available AI models
- `GET /api/examples` - Get search examples
- `POST /api/validate-key` - Validate API key

### Environment Variables

- `AIHUBMIX_API_KEY` - Main AI provider
- `OPENAI_API_KEY` - OpenAI API key
- `GOOGLE_API_KEY` - Google Gemini API key
- `ANTHROPIC_API_KEY` - Anthropic Claude API key

## Development Guidelines

### Code Style

- Use English for all code comments and commit messages
- Follow existing naming conventions
- Keep functions concise and well-documented

### Testing

- Use local test scripts in `/test-scripts/` directories
- Test scripts are ignored by Git (not uploaded to GitHub)
- Test encryption functionality locally before deployment

### Deployment

- Frontend builds to `dist/` directory
- Backend uses `render.yaml` for configuration
- Automatic deployment on Git push to master branch

### Common Issues

- CORS configuration for local development
- Encryption middleware must handle Chinese characters
- API timeouts set to 25s for AI calls, 10s for Scryfall

## File Locations

- Frontend encryption: `mtg-ai-frontend/src/utils/simpleEncryption.ts`
- Backend encryption: `mtg-ai-backend/app/simple_encryption.py`
- Middleware: `mtg-ai-backend/app/simple_middleware.py`
- Main API: `mtg-ai-backend/app/main.py`

## Testing Commands

```bash
# Frontend test
cd mtg-ai-frontend
# Open test-scripts/test_encryption.html in browser

# Backend test
cd mtg-ai-backend
python test-scripts/test_encryption.py
```

## Notes for AI Assistants

- Always check if changes affect encryption functionality
- Test with Chinese characters ("蓝色瞬间法术")
- Ensure CORS headers are properly set
- Keep test files local, don't commit to Git
- Use English for all documentation and comments
