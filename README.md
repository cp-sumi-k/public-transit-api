# public-transit-api

### API for providing scheduled transit services based on given data

## Overview
Implement a RESTful API to provide upcoming public transit service schedules between given origin and destination stations using the Metropolitan Transportation Authority(MTA) static GTFS data.

## Deployment

- This application is deployed using various AWS services like `AWS Lambda`, `API Gateway`, `ECR`, and `Cloudformation Stack`

- **ECR:** AWS Image registry for Docker image. [Built a public-transit-api using Docker and pushed to ECR](https://github.com/cp-sumi-k/public-transit-api/blob/main/scripts/ecr.sh)
- **AWS Lambda:** Serverless Microservice Service. Create a Lambda function using an ECR image
- **API gateway:** API routing service. Integrate Lambda proxy with API gateway REST API
- **Cloudformation Stack:** Infrastructure As Code(IAM) service. [Automate ECR image push and Lambda deployment](https://github.com/cp-sumi-k/public-transit-api/blob/main/infrastructure/lambda-template.yml)

## CI/CD Workflow

- [Test](https://github.com/cp-sumi-k/public-transit-api/blob/main/.github/workflows/test.yml)
- [Deployment](https://github.com/cp-sumi-k/public-transit-api/blob/main/.github/workflows/deploy.yml)

## Project Structure

- [`app`](https://github.com/cp-sumi-k/public-transit-api/tree/main/app): Main directory contains FastAPI application

- [`main.py`](https://github.com/cp-sumi-k/public-transit-api/blob/main/app/main.py): Entrypoint of the application contains the setup of FastAPI

- [`routes.py`](https://github.com/cp-sumi-k/public-transit-api/blob/main/app/routes.py): Have all API routes

- [`requirements.txt`](https://github.com/cp-sumi-k/public-transit-api/blob/main/requirements.txt): Index all the required dependencies for the project

- [`.env.example`](https://github.com/cp-sumi-k/public-transit-api/blob/main/app/.env.example): Have required env variables

- [`data`](https://github.com/cp-sumi-k/public-transit-api/tree/main/app/data): Contains MTA's static data

- [`gtfs_loader.py`](https://github.com/cp-sumi-k/public-transit-api/blob/main/app/gtfs_loader.py): Loader for loading MTA's data in the application

- [`transit.py`](https://github.com/cp-sumi-k/public-transit-api/blob/main/app/transit.py): Controller layer of app, provides logic for getting data

- [`model.py`](https://github.com/cp-sumi-k/public-transit-api/blob/main/app/model.py): Model layer of app, contains all required models

- [`utils.py`](https://github.com/cp-sumi-k/public-transit-api/blob/main/app/utils.py): Have all utility functions required in the app

- [`geocoding.py`](https://github.com/cp-sumi-k/public-transit-api/blob/main/app/geocoding.py): Google Maps API integration

- [`test`](https://github.com/cp-sumi-k/public-transit-api/tree/main/tests): Contains unit tests


## Run Application Locally

### Setup virtual environment

```sh
python -m venv .venv
```
```sh
source .venv/bin/activate
```

### Install required dependencies

```sh
pip install -r requirements.txt
```

### Go to APP Directory

```sh
cd app
```

### Setup environment variables

- Copy and set your env values in the .env file

```sh
cp .env.example .env
```

### Run API

```sh
python main.py
```

### Run tests

#### Create a directory for test_data

```sh
mkdir -p test_data/buses
```

#### Run Test
```sh
pytest
```

### API Documentation

- After running the application, you can find the API doc at `http://localhost:8000/redoc` or `http://localhost:8000/docs`.

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
