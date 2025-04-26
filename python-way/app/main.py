import sys
sys.path.append("..")
from fastapi import FastAPI
from app.db.database import engine,Base
from app.routers import user_routes, id_card_routes, coffee_routes
from app.utils.metadata import tags_metadata
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(engine)
app = FastAPI(
    title="caffeine API",
    description="API for caffeine project. A complete coffee ordering system that includes user management, ID card management, and coffee ordering.",
    version="0.1.0",
    openapi_tags=tags_metadata
)

# Allow all origins for now (for testing/development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. (You can specify specific domains later)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods like GET, POST, PUT, DELETE
    allow_headers=["*"],  # Allows all headers
)

app.include_router(user_routes.router, prefix="/api/auth")
app.include_router(id_card_routes.router, prefix="/api")
app.include_router(coffee_routes.router, prefix="/api/coffee")