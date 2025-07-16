#!/bin/bash

# AEO Assessment Tool Startup Script

echo "🚀 Starting AEO Assessment Tool..."

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo "❌ Error: backend/.env file not found!"
    echo "📝 Please copy backend/.env.example to backend/.env and add your Google API key"
    exit 1
fi

# Start backend server
echo "🔧 Starting backend server on port 8001..."
cd backend
python3 app.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend server
echo "🎨 Starting frontend server on port 3000..."
cd frontend
python3 -m http.server 3000 &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ AEO Assessment Tool is now running!"
echo ""
echo "📱 Frontend Interface: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8001"
echo "📚 API Documentation: http://localhost:8001/docs"
echo "💊 Health Check: http://localhost:8001/health"
echo ""
echo "📖 Documentation:"
echo "   📋 Current Features & Status: README.md"
echo "   🧠 Intelligence Analysis: AEO-Analysis-Logic.md"  
echo "   🚀 Development Roadmap: ROADMAP.md"
echo ""
echo "⚠️  Current Status: Basic tool (30% intelligence)"
echo "🎯 Target: Lite Intelligent AEO (70% intelligence)"
echo ""
echo "🛑 To stop the servers:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "📋 Press Ctrl+C to stop all servers"

# Wait for Ctrl+C
trap "echo ''; echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT

# Keep script running
wait 