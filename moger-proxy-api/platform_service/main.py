from fastapi import FastAPI
from mangum import Mangum
import logging

app = FastAPI()
logger = logging.getLogger()

@app.get("/")
async def greeting_world():
    return {"message": "hello world"}

handler = Mangum(app)

