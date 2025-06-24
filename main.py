from fastapi import FastAPI
import uvicorn
from db.database import engine
from db import models
from routes import api

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api.router, prefix="/auth", tags=["User"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
