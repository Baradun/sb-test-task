
pip install -r requirements.txt

export $(grep -v '^#' .env | xargs)

rm -f "$DATABASE_NAME"

pytest src/main_test.py

rm -f "$DATABASE_NAME"