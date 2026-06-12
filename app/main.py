from api import router
from fastapi import FastAPI

app = FastAPI(title="Learning RAG Demo")
app.include_router(router)
