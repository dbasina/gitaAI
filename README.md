# GitaAI

GitaAI is a web application built using Flask for the backend and React (Next.js) for the frontend. It provides spiritual guidance based on the Bhagavad Gita, integrating Elasticsearch for semantic search and OpenAI's GPT for generating meaningful insights.

---

## Features

- 🧠 **Semantic Search**: Search verses from the Bhagavad Gita using Elasticsearch.
- 🤖 **AI-Powered Insights**: Generate meaningful interpretations using GPT.
- ⚙️ **Integrated Frontend and Backend**: React (Next.js) serves as the frontend, and Flask handles API requests.
- 🐳 **Docker Support**: Easily deploy the project using Docker.

---
## Setup Instructions

### Prerequisites

- [Node.js](https://nodejs.org/) (version 18+ recommended)
- [Python](https://www.python.org/) (version 3.9+ recommended)
- [Docker](https://www.docker.com/) (optional, for containerized deployment)

---

### Backend (Flask)

1. Navigate to the backend directory:
   ```bash
   cd backend
   pip install -r requirements.txt
   python flask_app.py```

2. In a new terminal window:
   ```
   npm run dev
   ```
