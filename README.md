# public-transit-api

### API for providing scheduled transit services based on given data

## Overview
Implement RESTful API to provide upcoming public transit service’s schedules between given origin and destination stations using Metropolitan Transportation Authority(MTA) static GTFS data.

## Run Application

### Setup envrinment variables

- Copy and set your env values in .env file


```sh
cp .env.example .env
```

### Setup virtual environment

```sh
python -m venv .venv

source .venv/bin/activate
```

### Install required dependencies

```sh
pip install -r requirements.txt
```

### Run API

```sh
python main.py
```

### API Documentation

- After running application, you can find API doc at `http://localhost:8000/redoc`.

## Project Structure

- `main.py` : Entrypoint of the application contains setup of FastAPI

- `routes.py`: Have all API routes

- `requirements.txt` : Index all the require depenciens for the project

- `.env.example` : Have required env variables

- `gtfs`: Contains MTA's static data and loader for loading all data in the application

- `service`: Controller layer of app, provides logic of getting data

- `model`: Model layer of app, contains all required models

- `utils.py`: Have all utility functions required in app