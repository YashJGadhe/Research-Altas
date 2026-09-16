#!/bin/bash

# ResearchAtlas - Backend Startup Script
# This script helps diagnose and fix common issues

echo "🔍 ResearchAtlas Backend Diagnostic Tool"
echo "========================================"
echo ""

# Check if MongoDB is running
echo "1️⃣  Checking MongoDB..."
if pgrep -x "mongod" > /dev/null; then
    echo "   ✅ MongoDB is running"
else
    echo "   ❌ MongoDB is NOT running"
    echo "   💡 Start MongoDB with: mongod"
    echo ""
fi

# Check if virtual environment exists
echo "2️⃣  Checking virtual environment..."
if [ -d "venv" ]; then
    echo "   ✅ Virtual environment exists"
else
    echo "   ❌ Virtual environment NOT found"
    echo "   💡 Create it with: python -m venv venv"
    echo ""
fi

# Check if .env file exists
echo "3️⃣  Checking .env file..."
if [ -f ".env" ]; then
    echo "   ✅ .env file exists"
else
    echo "   ⚠️  .env file NOT found, creating from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "   ✅ Created .env from .env.example"
    else
        echo "   ❌ .env.example NOT found"
    fi
    echo ""
fi

# Check Python dependencies
echo "4️⃣  Checking Python dependencies..."
if [ -f "requirements.txt" ]; then
    echo "   ✅ requirements.txt exists"
    echo "   💡 Install with: pip install -r requirements.txt"
else
    echo "   ❌ requirements.txt NOT found"
fi
echo ""

# Check backend structure
echo "5️⃣  Checking backend structure..."
if [ -f "app/main.py" ]; then
    echo "   ✅ Backend structure looks good"
else
    echo "   ❌ Backend structure incomplete"
fi
echo ""

echo "========================================"
echo "🚀 To start the backend:"
echo ""
echo "   1. Start MongoDB: mongod"
echo "   2. Activate venv: source venv/bin/activate"
echo "   3. Install deps:  pip install -r requirements.txt"
echo "   4. Start backend: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "📝 Default admin credentials:"
echo "   Email: admin@raisoni.net"
echo "   Password: Admin@123"
echo ""
echo "🔧 If you still get errors, check the backend terminal for detailed logs."
echo ""
