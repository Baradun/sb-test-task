# Install dependencies from requirements.txt
pip install -r requirements.txt

# Set environment variables from the .env file
export $(grep -v '^#' .env | xargs)

# Remove database
rm -f "$DATABASE_NAME"

# Run Uvicorn
uvicorn src.main:app --reload --port $PORT --host $HOST