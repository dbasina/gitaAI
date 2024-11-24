# Step 1: Build the React frontend
FROM node:18 AS frontend
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build

# Step 2: Build the Flask backend
FROM python:3.12 AS backend
WORKDIR /app
COPY backend/ ./backend
COPY backend/requirements.txt ./requirements.txt
COPY --from=frontend /app/.next ./frontend
RUN pip install -r requirements.txt

# Step 3: Expose Flask API and Run
EXPOSE 5000
CMD ["python", "backend/flask_app.py"]
