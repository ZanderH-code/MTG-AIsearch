# MTG AI Search

An AI-powered Magic: The Gathering card search tool that helps players find cards using natural language descriptions.

## Features

- Natural language card search
- AI-powered card recommendations
- Advanced filtering options
- Real-time card information updates

## Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python (FastAPI)
- AI: OpenAI GPT models
- Database: Card data from Scryfall API

## Setup

1. Clone the repository
```bash
git clone https://github.com/ZanderH-code/MTG-AIsearch.git
cd MTG-AIsearch
```

2. Install backend dependencies
```bash
cd backend
pip install -r requirements.txt
```

3. Set up environment variables
```bash
cp env_example.txt .env
# Edit .env with your API keys
```

4. Run the application
```bash
python main.py
```

## Usage

1. Open `frontend/index.html` in your browser
2. Enter your card search query in natural language
3. View and filter the results

## License

MIT License