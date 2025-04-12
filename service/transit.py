from model.transit import TransitScheduleInput, TransitSchedule, TransitScheduleResponse
import math
from fastapi import HTTPException


def get_next_transit_schedules(state: any, input: TransitScheduleInput, page: int = 1, limit: int = 10) -> TransitScheduleResponse:
    try:
        loader = state.gtfs_loader
        geocoding_service = state.geocoding_service

        response: list[TransitSchedule] = []
        closest_stop = ""

        if input.origin_station_id:
            closest_stop = loader.get_closest_stop(
                input.origin_station_id)
            response = loader.get_schedule(
                input.origin_station_id, input.destination_station_id).to_dict(orient="records")

        elif input.coordinates:
            closest_stop = geocoding_service.reverse_geocode(
                input.coordinates.latitude, input.coordinates.longitude)
            origin_stop_id = loader.get_stop_id_from_coordinates(
                input.coordinates.latitude, input.coordinates.longitude)
            response = loader.get_schedule(
                origin_stop_id, input.destination_station_id).to_dict(orient="records")

        else:
            raise ValueError(
                "Either 'origin_station_id' or 'coordinates' must be provided.")

        # paginate
        total_schedules = len(response)
        total_pages = math.ceil(total_schedules / limit)
        skip = (page - 1) * limit
        response = response[skip:skip + limit]

        return TransitScheduleResponse(
            total_schedules=total_schedules,
            total_pages=total_pages,
            current_page=page,
            closest_stop=closest_stop,
            next_schedules=response
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
