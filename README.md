# MetaReview - Meta-Analysis Tool for Researchers

MetaReview is a web application that helps researchers find papers, code them with AI assistance, and produce final tables for meta-analysis purposes.

## Features

- **Paper Search & Import**: Search for academic papers via OpenAlex and import them into your projects
- **PDF Viewing & Coding**: View PDFs and extract data using customizable coding sheets
- **AI-Assisted Coding**: Use AI to help extract relevant data from papers
- **Results Tables**: Generate tables for meta-analysis from your coded data
- **Team Collaboration**: Work with colleagues on the same project (coming soon)

## Project Structure

- `/api_docs` - Documentation for external APIs
- `/backend` - Python FastAPI backend
- `/frontend` - Vue.js frontend
- `/docs` - Project documentation

## Getting Started

### Prerequisites

- Node.js (v16+)
- Python (3.8+)
- pip

### Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install pydantic-settings
uvicorn main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm install @fortawesome/fontawesome-svg-core @fortawesome/free-solid-svg-icons @fortawesome/vue-fontawesome
npm run dev
```

The application will be available at http://localhost:5173

## API Configuration

The application uses the OpenAlex API for academic paper searches. For better performance, set your email in the `.env` file:

```
OPENALEX_EMAIL=your.email@example.com
```

This will place you in the OpenAlex "polite pool" for better rate limits.

## Current Status

This project is under active development. See the [PROJECT_TRACKER.md](./PROJECT_TRACKER.md) file for the current status and upcoming tasks.

## License

MIT
