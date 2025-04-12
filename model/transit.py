from pydantic import BaseModel


class Coordinates(BaseModel):
    latitude: float | None = None
    longitude: float | None = None


class TransitScheduleInput(BaseModel):
    origin_station_id: str
    destination_station_id: str
    coordinates: Coordinates | None = None


class TransitSchedule(BaseModel):
    transit_mode: str
    eta_origin: str
    eta_destination: str
