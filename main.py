import uvicorn
from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict


# Get settings from .env file
class Settings(BaseSettings):
    server_port: int
    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.server_port)
