#!/bin/bash

# Enhanced startup script for Gift Guru with Amazon integration
# Author: MiniMax Agent

echo "🚀 Starting Gift Guru - Amazon Integrated Edition"
echo "============================================="

# Check if we're in the right directory
if [ ! -d "frontend" ] || [ ! -d "backend" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Function to check if port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "⚠️  Port $port is already in use"
        return 1
    fi
    return 0
fi

# Function to install dependencies
install_deps() {
    echo "📦 Installing dependencies..."
    
    # Backend dependencies
    echo "Installing backend dependencies..."
    cd backend
    
    if [ -f "enhanced_requirements.txt" ]; then
        pip install -r enhanced_requirements.txt
    else
        pip install -r requirements.txt
    fi
    
    cd ..
    
    # Frontend dependencies
    echo "Installing frontend dependencies..."
    cd frontend
    
    if [ ! -d "node_modules" ]; then
        npm install
    fi
    
    cd ..
}

# Function to check Amazon API setup
check_amazon_setup() {
    echo "🔍 Checking Amazon API setup..."
    
    if [ -f "backend/.env" ]; then
        echo "✅ Environment file found"
        
        # Check if credentials are set (not just placeholder values)
        if grep -q "your_amazon_api_key_here" backend/.env 2>/dev/null; then
            echo "⚠️  Amazon credentials not configured (using placeholders)"
            echo "   Edit backend/.env with your actual Amazon API credentials"
            echo "   See AMAZON_SETUP_GUIDE.md for detailed instructions"
        else
            echo "✅ Amazon credentials configured"
        fi
    else
        echo "⚠️  No .env file found"
        echo "   Copying .env.example to .env..."
        cp backend/.env.example backend/.env
        echo "   Please edit backend/.env with your Amazon API credentials"
        echo "   See AMAZON_SETUP_GUIDE.md for setup instructions"
    fi
    
    # Check if amazon-paapi is installed
    if python3 -c "import amazon_paapi" 2>/dev/null; then
        echo "✅ Amazon API SDK installed"
    else
        echo "⚠️  Amazon API SDK not installed"
        echo "   Installing python-amazon-paapi..."
        pip install python-amazon-paapi
    fi
}

# Function to start backend
start_backend() {
    echo "🔗 Starting Enhanced Backend (Port 8000)..."
    
    cd backend
    
    # Use enhanced API if available, fallback to original
    if [ -f "enhanced_api.py" ]; then
        python3 enhanced_api.py &
    else
        python3 api.py &
    fi
    
    BACKEND_PID=$!
    cd ..
    
    echo "Backend PID: $BACKEND_PID"
    
    # Wait a moment for backend to start
    sleep 3
    
    # Test backend connectivity
    if curl -s "http://localhost:8000" > /dev/null 2>&1; then
        echo "✅ Backend started successfully"
    else
        echo "❌ Backend failed to start properly"
        return 1
    fi
}

# Function to start frontend
start_frontend() {
    echo "🎨 Starting React Frontend (Port 3000)..."
    
    cd frontend
    
    # Set environment variables for React
    export REACT_APP_API_URL="http://localhost:8000"
    export REACT_APP_VERSION="2.0.0-amazon"
    
    npm start &
    FRONTEND_PID=$!
    cd ..
    
    echo "Frontend PID: $FRONTEND_PID"
    
    # Wait for frontend to start
    echo "Waiting for frontend to start..."
    sleep 5
    
    if curl -s "http://localhost:3000" > /dev/null 2>&1; then
        echo "✅ Frontend started successfully"
    else
        echo "⚠️  Frontend may still be starting up..."
    fi
}

# Function to show status
show_status() {
    echo ""
    echo "🎆 Gift Guru - Amazon Integrated is running!"
    echo "=========================================="
    echo ""
    echo "🎨 Frontend:     http://localhost:3000"
    echo "🔗 Backend API:   http://localhost:8000"
    echo "📊 API Docs:     http://localhost:8000/docs"
    echo "🛒 Amazon Status: http://localhost:8000/amazon-status"
    echo ""
    echo "📱 Features Available:"
    echo "   • Live Amazon product search"
    echo "   • AI-powered recommendations"
    echo "   • Real-time pricing and ratings"
    echo "   • Interactive rating system"
    echo "   • Malayalam humor integration"
    echo "   • Mobile-responsive design"
    echo ""
    echo "🛑 To stop: Press Ctrl+C"
    echo ""
}

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "📋 Shutting down Gift Guru..."
    
    # Kill background processes
    if [ ! -z "$BACKEND_PID" ]; then
        echo "Stopping backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID 2>/dev/null
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        echo "Stopping frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID 2>/dev/null
    fi
    
    # Kill any remaining processes on our ports
    fuser -k 8000/tcp 2>/dev/null
    fuser -k 3000/tcp 2>/dev/null
    
    echo "✅ Cleanup complete"
    echo "👋 Thank you for using Gift Guru!"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Main execution
echo "Starting enhanced Gift Guru with Amazon integration..."

# Check ports
if ! check_port 8000; then
    echo "Killing process on port 8000..."
    fuser -k 8000/tcp 2>/dev/null
    sleep 2
fi

if ! check_port 3000; then
    echo "Killing process on port 3000..."
    fuser -k 3000/tcp 2>/dev/null
    sleep 2
fi

# Install dependencies if needed
echo "🔧 Checking dependencies..."
install_deps

# Check Amazon API setup
check_amazon_setup

# Start services
if start_backend; then
    start_frontend
    show_status
    
    # Keep script running
    echo "⏳ Services running... (Press Ctrl+C to stop)"
    while true; do
        sleep 1
    done
else
    echo "❌ Failed to start backend, aborting..."
    exit 1
fi
