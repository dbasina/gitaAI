# GitaAI

GitaAI is a web application built using Flask for the backend and React (Next.js) for the frontend. It provides spiritual guidance based on the Bhagavad Gita, integrating Elasticsearch for semantic search and OpenAI's GPT for generating meaningful insights.

---

## Features

- 🧠 **Semantic Search**: Search verses from the Bhagavad Gita using Elasticsearch.
- 🤖 **AI-Powered Insights**: Generate meaningful interpretations using GPT.
- ⚙️ **Integrated Frontend and Backend**: React (Next.js) serves as the frontend, and Flask handles API requests.
- 🐳 **Docker Support**: Easily deploy the project using Docker.

---

## Project Structure

my-app/ ├── app/ # React (Next.js) frontend │ ├── .next/ # Build output │ ├── public/ # Static assets │ ├── src/ # Source code │ │ ├── components/ # React components │ │ ├── pages/ # Next.js pages │ │ └── styles/ # Styles │ ├── package.json # Frontend dependencies │ └── next.config.js # Next.js configuration ├── backend/ # Flask backend │ ├── flask_app.py # Flask application │ ├── requirements.txt # Python dependencies │ └── utils/ # Utility functions ├── Dockerfile # Docker configuration ├── docker-compose.yml # Multi-service setup ├── README.md # Documentation └── .gitignore # Ignored files

yaml
Copy code

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
Create a virtual environment (optional but recommended):

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
Install Python dependencies:

bash
Copy code
pip install -r requirements.txt
Run the Flask application:

bash
Copy code
python flask_app.py
Access the backend API at:

arduino
Copy code
http://localhost:5000
Frontend (React)
Navigate to the app directory:

bash
Copy code
cd app
Install dependencies:

bash
Copy code
npm install
Start the development server:

bash
Copy code
npm run dev
Access the React frontend at:

arduino
Copy code
http://localhost:3000
Docker Deployment
Build the Docker image:

bash
Copy code
docker build -t flask-react-demo .
Run the Docker container:

bash
Copy code
docker run -p 5000:5000 flask-react-demo
Access the application at:

arduino
Copy code
http://localhost:5000
API Endpoints
POST /api/gita
Description: Accepts a query and returns AI-generated insights based on the Bhagavad Gita.
Request Body:
json
Copy code
{
  "query": "What does the Gita say about duty?"
}
Response:
json
Copy code
{
  "response": "Your query was: What does the Gita say about duty?"
}
Built With
Flask - Backend framework
React (Next.js) - Frontend framework
Elasticsearch - Search engine
OpenAI GPT - AI text generation
Docker - Containerization
Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.
Create a new branch for your feature or bug fix:
bash
Copy code
git checkout -b feature-name
Commit your changes:
bash
Copy code
git commit -m "Add your message here"
Push to the branch:
bash
Copy code
git push origin feature-name
Open a Pull Request.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Inspired by the teachings of the Bhagavad Gita.
Powered by OpenAI and Elasticsearch.