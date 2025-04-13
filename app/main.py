import uvicorn
from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict
from contextlib import asynccontextmanager
from routes import router as api_router
from geocoding import GeocodingService
from gtfs_loader import GTFSLoader
from mangum import Mangum


# Get settings from .env file
class Settings(BaseSettings):
    server_port: int
    google_maps_api_key: str
    model_config = SettingsConfigDict(env_file='.env')


gtfs_cache = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    if 'data' not in gtfs_cache:
        print("Loading GTFS data...")
        # Load GTFS data once on startup
        loader = GTFSLoader(root_data_dir="data")
        data = loader.load_all()
        gtfs_cache["data"] = data
        gtfs_cache["loader"] = loader

    app.state.gtfs_loader = gtfs_cache["loader"]

    geocoding_service = GeocodingService(
        api_key=settings.google_maps_api_key
    )
    app.state.geocoding_service = geocoding_service

    yield


settings = Settings()
app = FastAPI(lifespan=lifespan)
app.include_router(api_router)

handler = Mangum(app)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.server_port)
