from contextlib import asynccontextmanager
import asyncio
from src.core.scheduler import price_fetch_worker
from fastapi import FastAPI
from src.router.asset_router import router as asset_router
from src.router.analytics_router import router as analytics_router
from src.db.database import create_all_tables 

worker_task = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Attempting to create database tables...")
    try:
        await create_all_tables()
    except Exception as e:
        print(f"ERROR: Failed to create database tables: {e}") 
    
    global worker_task
    print("Starting background price worker...")
    worker_task = asyncio.create_task(price_fetch_worker())
    
    yield
    
    print("Shutting down background price worker...")
    if worker_task:
        worker_task.cancel()
        try:
            await worker_task
        except asyncio.CancelledError:
            pass

app = FastAPI(
    title="A Crypto-API",
    lifespan=lifespan
)

app.include_router(asset_router)
app.include_router(analytics_router)

@app.get("/",tags=["Root"])
def root():
    return {
        "message" : "Welcome!"
    }