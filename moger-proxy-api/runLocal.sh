export $(grep -v '^#' .env | xargs)
poetry run uvicorn platform_service.main:app --reload