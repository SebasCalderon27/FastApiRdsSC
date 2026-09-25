from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import init_db
from app.routers import users, products

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="API con FastAPI, AWS EC2 y RDS",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(users.router)
app.include_router(products.router)

@app.get("/")
def root():
    return {"status": "API corriendo", "docs": "/docs"}