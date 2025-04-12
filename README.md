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

## Project Structure

- main.py : Entrypoint of the application contains setupo of FastAPI

- requirements.txt : Index all the require depenciens for the project

- .env.example : Have required env variables
