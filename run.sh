#!/bin/bash
# Stop any existing processes on ports 8000 and 3000
kill $(lsof -t -i :8000) 2>/dev/null || true
kill $(lsof -t -i :3000) 2>/dev/null || true

echo "Starting Backend..."
cd backend
python3 main.py > backend.log 2>&1 &
cd ..

echo "Starting Frontend..."
cd frontend
python3 -m http.server 3000 > frontend.log 2>&1 &
cd ..

echo "Services started!"
echo "- Frontend: http://localhost:3000/index.html"
echo "- Backend API: http://localhost:8000/api/popular"
