from pydantic import BaseModel, model_validator
from typing import Optional

class Coordinates(BaseModel):
    latitude: float | None = None
    longitude: float | None = None


class TransitScheduleInput(BaseModel):
    origin_station_id: Optional[str] = None
    destination_station_id: str
    coordinates: Optional[Coordinates] = None

    @model_validator(mode="after")
    def check_either_origin_or_coordinates(self):
        origin = self.origin_station_id
        coords = self.coordinates
        if not origin and not coords:
            raise ValueError(
                "Either 'origin_station_id' or 'coordinates' must be provided.")
        return self

class TransitSchedule(BaseModel):
    trip_id: str
    transit_mode: str
    eta_origin: str
    eta_destination: str


class TransitScheduleResponse(BaseModel):
    total_schedules: int
    total_pages: int
    current_page: int
    next_schedules: list[TransitSchedule]
