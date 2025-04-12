import uvicorn
from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict
from gtfs.loader import GTFSLoader
from contextlib import asynccontextmanager
from routes import router as api_router


# Get settings from .env file
class Settings(BaseSettings):
    server_port: int
    model_config = SettingsConfigDict(env_file='.env')


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load GTFS data once on startup
    loader = GTFSLoader(root_data_dir="gtfs/data")
    loader.load_all()
    app.state.gtfs_loader = loader
    yield


settings = Settings()
app = FastAPI(lifespan=lifespan)
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.server_port)
