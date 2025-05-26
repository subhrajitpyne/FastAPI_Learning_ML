from fastapi import FastAPI

app: FastAPI  = FastAPI()

@app.get("/")
async def first_api() -> dict:
    return {'message': 'Hello Subhrajit'}

@app.get("/ankita")
async def first_api() -> dict:
    return {'message': 'Hello ankita'}