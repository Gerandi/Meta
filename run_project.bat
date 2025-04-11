@echo off
echo Starting MetaReview Project...
echo.
echo ----- MetaReview Project Update -----
echo Fixed issues and new features:
echo 1. Fixed [object Object] error when selecting a specific database
echo 2. Improved search result relevance
echo 3. Fixed pagination issues - now faster and more consistent
echo 4. Enhanced filtering in search results
echo 5. Improved "Add to Collection" functionality
echo 6. Better error handling throughout the application
echo See implementation_notes.md for details
echo -------------------------------------
echo.

echo Installing required dependencies...
cd backend
pip install -r requirements.txt 2>nul
pip install pydantic-settings 2>nul
cd ..

echo Creating database if it doesn't exist...
cd backend
python setup_db.py
cd ..

echo Starting backend (in a new window)...
start cmd /k "cd backend && run_backend.bat"

echo Starting frontend (in this window)...
cd frontend && npm install
cd frontend && run_frontend.bat
