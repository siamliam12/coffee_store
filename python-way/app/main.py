import sys
sys.path.append("..")
from fastapi import FastAPI
from app.db.database import engine,SessionLocal,Base
from app.routers import user_routes
from app.models import user_model

app = FastAPI()
Base.metadata.create_all(engine)
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

app.include_router(user_routes.router, prefix="/api/auth")