#!/bin/bash

# Development startup script for Gift Guru
# Starts both services with development settings

echo "👨‍💻 Gift Guru - Development Mode"
echo "=============================="

# Start backend with hot reload
echo "🔄 Starting backend with auto-reload..."
cd backend
uvicorn api:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Start frontend with development server
echo "🔄 Starting frontend with hot reload..."
cd ../frontend
REACT_APP_DEBUG=true npm start &
FRONTEND_PID=$!

# Function to cleanup on exit
cleanup() {
    echo "
🛱 Stopping development servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

echo ""
echo "🏁 Development servers started!"
echo "💻 Frontend: http://localhost:3000 (React Dev Server)"
echo "🔗 Backend: http://localhost:8000 (FastAPI with auto-reload)"
echo "📄 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

wait