@echo off
echo Starting MetaReview Project...
echo.
echo ----- MetaReview Project Update -----
echo Fixed issues:
echo 1. Fixed [object Object] error when selecting a specific database
echo 2. Improved search result relevance
echo 3. Fixed pagination issues - now faster and more consistent
echo See implementation_notes.md for details
echo -------------------------------------
echo.

echo Installing required dependencies...
cd backend
pip install -r requirements.txt 2>nul
pip install pydantic-settings 2>nul
cd ..

echo Starting backend (in a new window)...
start cmd /k "cd backend && run_backend.bat"

echo Starting frontend (in this window)...
cd frontend && run_frontend.bat
