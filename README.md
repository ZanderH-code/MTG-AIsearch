# MTG AI Search

A powerful Magic: The Gathering card search application that combines AI-powered natural language processing with the Scryfall API to provide intelligent card discovery.

## 🌟 Features

### Core Functionality

- **AI-Powered Search**: Convert natural language queries into Scryfall search syntax using AI models
- **Multi-Language Support**: Full Chinese and English interface with dynamic language switching
- **High-Quality Card Display**: Clear card images with detailed information
- **Direct Scryfall Integration**: Click any card to view full details on Scryfall
- **Dark Theme**: Modern dark interface for better user experience

### Technical Features

- **Separate Frontend/Backend Architecture**: Independent deployment for better scalability
- **Cloud Deployment**: Fully deployed on Render.com
- **API Key Management**: Secure local storage of API keys
- **Multiple AI Providers**: Support for Aihubmix and OpenAI APIs
- **Responsive Design**: Works on desktop and mobile devices

## 🏗️ Architecture

### Project Structure

```
MTG-AIsearch/
├── mtg-ai-backend/          # FastAPI backend service
│   ├── app/
│   │   ├── main.py         # Main API endpoints
│   │   └── __init__.py     # Package initialization
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile         # Container configuration
│   └── render.yaml        # Render deployment config
├── mtg-ai-frontend/        # Static frontend application
│   ├── build/
│   │   ├── index.html     # Main search interface
│   │   └── login.html     # API key configuration
│   ├── package.json       # Node.js dependencies
│   └── render.yaml        # Render static site config
└── README.md              # This file
```

### Technology Stack

- **Backend**: FastAPI, Python 3.9, Uvicorn
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **AI Integration**: Aihubmix API, OpenAI API
- **Card Database**: Scryfall API
- **Deployment**: Render.com (Docker + Static Site)
- **Version Control**: Git with submodules

## 🚀 Deployment

### Backend (mtg-ai-backend)

- **Platform**: Render.com Web Service
- **Environment**: Docker
- **Region**: Singapore
- **URL**: https://mtg-ai-backend.onrender.com

### Frontend (mtg-ai-frontend)

- **Platform**: Render.com Static Site
- **Region**: Singapore
- **URL**: https://mtg-ai-frontend.onrender.com

## 📋 API Endpoints

### Core Endpoints

- `GET /` - Health check
- `GET /health` - Service status
- `GET /api/models` - Get available AI models
- `POST /api/validate-key` - Validate API key
- `POST /api/search` - Search MTG cards

### Search Request Format

```json
{
  "query": "green creatures with power 4+",
  "language": "en",
  "api_key": "your-api-key",
  "model": "gpt-4o-mini"
}
```

### Search Response Format

```json
{
  "cards": [
    {
      "name": "Card Name",
      "mana_cost": "{2}{G}",
      "type_line": "Creature — Beast",
      "oracle_text": "Card rules text...",
      "image_uris": {
        "small": "url",
        "normal": "url"
      },
      "scryfall_uri": "https://scryfall.com/card/..."
    }
  ],
  "scryfall_query": "t:creature c:g pow>=4",
  "total_cards": 25,
  "api_provider": "aihubmix"
}
```

## 🔧 Setup and Configuration

### Prerequisites

- Python 3.9+
- Node.js (for local development)
- API keys for AI services (Aihubmix or OpenAI)

### Local Development

#### Backend Setup

```bash
cd mtg-ai-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend Setup

```bash
cd mtg-ai-frontend
npm install
npx serve build
```

### Environment Variables

```bash
# Backend environment variables (set in Render dashboard)
OPENAI_API_KEY=your-openai-key
AIHUBMIX_API_KEY=your-aihubmix-key
```

## 🎯 Usage

### Getting Started

1. Visit the frontend application
2. Configure your API key in the settings
3. Enter natural language search queries
4. Click on cards to view full details on Scryfall

### Example Queries

- **English**: "red creatures with haste"
- **Chinese**: "具有敏捷的红色生物"
- **Complex**: "landfall creatures that win the game"
- **Color-based**: "blue white control spells"

### Supported Search Types

- **Card Types**: creatures, instants, sorceries, artifacts, enchantments, planeswalkers, lands
- **Colors**: white, blue, black, red, green, and combinations
- **Keywords**: landfall, haste, flying, etc.
- **Power/Toughness**: specific values or ranges
- **Mana Value**: specific costs or ranges
- **Rarity**: common, uncommon, rare, mythic

## 🔒 Security

- API keys are stored locally in browser localStorage
- No sensitive data is stored on the server
- HTTPS encryption for all communications
- CORS properly configured for cross-origin requests

## 🌐 Language Support

### Interface Languages

- **Chinese (中文)**: Full interface translation
- **English**: Complete English localization

### Input Languages

- **Chinese**: Natural language queries in Chinese
- **English**: Natural language queries in English

### Dynamic Switching

- Toggle between languages without page reload
- All UI elements update instantly
- Search examples adapt to selected language

## 🎨 UI/UX Features

### Dark Theme

- Modern dark color scheme
- High contrast for readability
- Consistent color palette throughout
- Hover effects and smooth transitions

### Card Display

- High-quality card images
- Clear typography and spacing
- Clickable cards for Scryfall navigation
- Responsive grid layout

### User Experience

- Loading states and progress indicators
- Error handling with user-friendly messages
- Keyboard navigation support
- Mobile-responsive design

## 🔄 Recent Updates

### Latest Improvements

- Removed redundant "click to view details" text for cleaner design
- Enhanced card image quality using normal resolution
- Improved dark theme color contrast
- Added comprehensive language switching functionality
- Implemented direct Scryfall card linking

## 📈 Performance

### Optimization Features

- Efficient API calls with proper caching
- Optimized image loading with fallbacks
- Minimal bundle size for fast loading
- CDN delivery for static assets

### Monitoring

- Health check endpoints for service monitoring
- Error logging and debugging information
- Performance metrics tracking

## 🤝 Contributing

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Standards

- Follow PEP 8 for Python code
- Use consistent JavaScript formatting
- Maintain responsive design principles
- Ensure accessibility compliance

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Scryfall**: For providing the comprehensive MTG card database API
- **Aihubmix**: For AI model access and natural language processing
- **OpenAI**: For alternative AI model support
- **Render.com**: For reliable cloud hosting services

## 📞 Support

For issues, questions, or contributions:

- Create an issue on GitHub
- Check the deployment logs on Render.com
- Review the API documentation for troubleshooting

---

**Built with ❤️ for the Magic: The Gathering community**
