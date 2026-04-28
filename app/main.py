from fastapi import FastAPI
from .database import Base, engine
from .routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AR Data Engine")

app.include_router(router)