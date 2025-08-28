# 🎴 MTG AI Search Tool

An AI-powered Magic: The Gathering card search tool with natural language search and intelligent sorting.

## ✨ Features

- **🤖 AI-Powered Search**: Search cards using natural language descriptions
- **🌙 Dark Theme**: Modern dark interface design with Tailwind CSS
- **🌍 Multi-language Support**: Chinese and English interfaces
- **📊 Smart Sorting**: Multiple sorting options (name, rarity, mana value, etc.)
- **💡 Search Examples**: Common search examples provided
- **🔗 Direct Links**: Click cards to jump directly to Scryfall
- **🔒 API Key Protection**: Secure API key handling with masking
- **⚡ Multiple AI Providers**: Support for OpenAI, AIHubMix, Google Gemini, and Anthropic Claude

## 🚀 Live Demo

- **Frontend App**: https://mtg-ai-frontend.onrender.com
- **Backend API**: https://mtg-ai-backend.onrender.com

## 📁 Project Structure

```
demo/
├── mtg-ai-frontend/     # React + TypeScript + Vite frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API services
│   │   ├── types/       # TypeScript type definitions
│   │   └── utils/       # Utility functions
│   ├── package.json
│   └── vite.config.ts
└── mtg-ai-backend/      # Python FastAPI backend
    ├── app/
    │   ├── main.py      # Main API endpoints
    │   ├── preprocessor.py  # Query preprocessing
    │   └── simple_encryption.py  # API key protection
    ├── requirements.txt
    └── render.yaml
```

## 🛠️ Tech Stack

### Frontend
- **React 18** with TypeScript
- **Vite** for build tooling
- **Tailwind CSS** for styling
- **Axios** for API communication
- **LocalStorage** for state persistence

### Backend
- **Python 3.12** with FastAPI
- **httpx** for async HTTP requests
- **pydantic** for data validation
- **Scryfall API** integration
- **Multiple AI providers** (OpenAI, AIHubMix, Google, Anthropic)

## 🔧 Project Workflow

### 1. User Interface Flow
1. **Landing Page**: User sees search interface with examples
2. **Settings Configuration**: User configures API key and selects AI provider
3. **Natural Language Search**: User enters search query in Chinese or English
4. **AI Processing**: Backend converts natural language to Scryfall syntax
5. **Card Search**: Scryfall API returns matching cards
6. **Results Display**: Frontend displays cards with sorting options
7. **Card Details**: Click cards to view details on Scryfall

### 2. Backend Processing Flow
1. **Request Reception**: FastAPI receives search request
2. **Query Preprocessing**: Chinese terms are mapped to English equivalents
3. **AI API Call**: Natural language is sent to AI provider
4. **Scryfall Query Generation**: AI returns Scryfall search syntax
5. **Card Search**: Scryfall API is queried with generated syntax
6. **Response Processing**: Cards are sorted and formatted
7. **Result Return**: Processed data is sent back to frontend

### 3. AI Integration Flow
1. **Provider Selection**: User chooses AI provider (AIHubMix recommended)
2. **Model Selection**: Available models are fetched from provider
3. **API Key Validation**: Backend validates API key with provider
4. **Query Processing**: Natural language is processed by AI model
5. **Response Parsing**: AI response is converted to Scryfall syntax

## 🚀 Local Development Setup

### Prerequisites
- Node.js 18+ and npm/yarn
- Python 3.12+
- Git

### Frontend Setup
```bash
cd mtg-ai-frontend
npm install
npm run dev
# Frontend will be available at http://localhost:5173
```

### Backend Setup
```bash
cd mtg-ai-backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# Backend will be available at http://localhost:8000
```

### Environment Variables
Create `.env` file in backend directory:
```env
AIHUBMIX_API_KEY=your_aihubmix_api_key
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

## 📖 Usage Examples

### Search Examples
- **中文**: "蓝色瞬间法术" → Search for blue instant spells
- **中文**: "红色生物 力量大于4" → Search for red creatures with power > 4
- **English**: "green creatures" → Search for green creature cards
- **English**: "red burn spells" → Search for red damage spells
- **English**: "esper control" → Search for Esper color control cards

### Sorting Features
- **By Name**: Alphabetical order (A-Z or Z-A)
- **By Rarity**: Common → Uncommon → Rare → Mythic (asc) or reverse (desc)
- **By Mana Value**: Sort by converted mana cost
- **By Color**: Sort by color identity
- **By Power/Toughness**: Sort by creature stats
- **By Set**: Sort by release set
- **By Artist**: Sort by card artist

## 🔑 API Configuration

1. Visit the frontend app
2. Click the "Settings" button (gear icon)
3. Select your preferred AI provider
4. Enter your API key
5. Click "Validate" to test the key
6. Select your preferred AI model
7. Click "Save" to store settings

### Recommended Setup
- **Provider**: AIHubMix (provides access to multiple AI models)
- **Model**: gpt-4o-mini (good balance of performance and cost)

## 🔒 Security Features

- **API Key Masking**: All API keys are masked in logs and console output
- **CORS Protection**: Proper CORS configuration for secure communication
- **Input Validation**: All user inputs are validated using Pydantic
- **Error Handling**: Comprehensive error handling with user-friendly messages

## 🚀 Deployment

### Frontend (Render)
- Build command: `yarn install && yarn build`
- Publish directory: `./dist`
- Environment: Static site

### Backend (Render)
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Environment: Python 3.12

## 📝 License

MIT License

## 🤝 Contributing

Issues and Pull Requests are welcome!

---

**Enjoy your Magic: The Gathering search experience!** 🎴✨
