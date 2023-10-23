export $(grep -v '^#' .env | xargs)
poetry run uvicorn platform_service.main:app --reload --port 5362