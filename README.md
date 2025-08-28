# 🎴 MTG AI Search Tool

An AI-powered Magic: The Gathering card search tool with natural language search and intelligent sorting.

## ✨ Features

- **🤖 AI-Powered Search**: Search cards using natural language descriptions
- **🌙 Dark Theme**: Modern dark interface design
- **🌍 Multi-language Support**: Chinese and English interfaces
- **📊 Smart Sorting**: Multiple sorting options (name, rarity, mana value, etc.)
- **💡 Search Examples**: Common search examples provided
- **🔗 Direct Links**: Click cards to jump directly to Scryfall

## 🚀 Live Demo

- **Frontend App**: https://mtg-ai-frontend.onrender.com
- **Backend API**: https://mtg-ai-backend.onrender.com

## 📁 Project Structure

```
MTG-AIsearch/
├── mtg-ai-frontend/    # Frontend project (HTML/CSS/JS)
└── mtg-ai-backend/     # Backend project (Python FastAPI)
```

## 🛠️ Tech Stack

### Frontend

- HTML5 + CSS3 + JavaScript
- Responsive design
- Dark theme UI

### Backend

- Python FastAPI
- Scryfall API integration
- OpenAI/AIHubMix API support

## 🔧 Local Development

### Frontend Development

```bash
cd mtg-ai-frontend
# Frontend is static files, just open build/index.html
```

### Backend Development

```bash
cd mtg-ai-backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 📖 Usage Examples

### Search Examples

- "green creatures" → Search for green creature cards
- "red burn spells" → Search for red damage spells
- "esper control" → Search for Esper color control cards
- "creatures with power 4+" → Search for creatures with power 4 or greater

### Sorting Features

- **By Name**: Alphabetical order
- **By Rarity**: Mythic → Rare → Uncommon → Common
- **By Mana Value**: Sort by mana cost
- **By Color**: Sort by color identity
- **By Power/Toughness**: Sort by creature stats

## 🔑 API Configuration

1. Visit the frontend app
2. Click the "Settings" button
3. Configure your AI API key (OpenAI or AIHubMix)
4. Start using AI search features

## 📝 License

MIT License

## 🤝 Contributing

Issues and Pull Requests are welcome!

---

**Enjoy your Magic: The Gathering search experience!** 🎴✨
