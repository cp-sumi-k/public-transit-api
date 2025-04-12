# public-transit-api

### API for providing scheduled transit services based on given data

## Overview
Implement RESTful API to provide upcoming public transit service’s schedules between given origin and destination stations using Metropolitan Transportation Authority(MTA) static GTFS data.

## Run Application Locally

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

## Run API

API URL: `http://localhost:8000/api/v1/transit/schedules?page=1&limit=10`

Method: `POST`

Request: 

```json
{
    "origin_station_id": "103391",
    "coordinates": {
        "latitude": 40.85,
        "longitude": -73.89
    },
    "destination_station_id": "103392"
}
```

## Project Structure

- `main.py` : Entrypoint of the application contains setup of FastAPI

- `routes.py`: Have all API routes

- `requirements.txt` : Index all the require depenciens for the project

- `.env.example` : Have required env variables

- `data`: Contains MTA's static data

- `gtfs_loader.py`: Loader for loading MTA's data in the application

- `transit.py`: Controller layer of app, provides logic of getting data

- `model.py`: Model layer of app, contains all required models

- `utils.py`: Have all utility functions required in app

- `geocoding.py ` : Google Maps API integration

- `test`: Contains unit tests

- `test_data`: Scaffolded folder for test data of unit tests