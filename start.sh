#!/bin/bash

# Gift Guru - Full Stack Startup Script
# Starts both React frontend and FastAPI backend

echo "🎁 Starting Gift Guru - Full Stack Application"
echo "================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Install backend dependencies
echo "🐍 Installing Python backend dependencies..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
echo "✅ Backend dependencies installed"

# Start backend in background
echo "🚀 Starting FastAPI backend on port 8000..."
uvicorn api:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Install frontend dependencies
echo "⚙️ Installing React frontend dependencies..."
cd ../frontend
if [ ! -d "node_modules" ]; then
    npm install
fi
echo "✅ Frontend dependencies installed"

# Start frontend
echo "🚀 Starting React frontend on port 3000..."
echo "🎉 Gift Guru will open in your browser shortly!"
echo "💻 Frontend: http://localhost:3000"
echo "🔗 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"

npm start &
FRONTEND_PID=$!

# Function to cleanup on exit
cleanup() {
    echo "
🛱 Shutting down Gift Guru..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Cleanup complete. Goodbye!"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

echo ""
echo "🎁 Gift Guru is running!"
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for user interruption
wait