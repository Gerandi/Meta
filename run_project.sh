#!/bin/bash
echo "Starting MetaReview Project..."

echo "Installing required dependencies..."
cd backend
pip install -r requirements.txt >/dev/null 2>&1
pip install pydantic-settings >/dev/null 2>&1
cd ..

echo "Starting backend (in a new window)..."
gnome-terminal -- bash -c "cd backend && bash run_backend.sh" || \
xterm -e "cd backend && bash run_backend.sh" || \
osascript -e 'tell app "Terminal" to do script "cd '$(pwd)'/backend && bash run_backend.sh"'

echo "Starting frontend (in this window)..."
cd frontend && npm install && npm run dev
