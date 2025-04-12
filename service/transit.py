from model.transit import TransitScheduleInput, TransitSchedule, TransitScheduleResponse
import math
from fastapi import HTTPException


def get_next_transit_schedules(state: any, input: TransitScheduleInput, page: int = 1, limit: int = 10) -> TransitScheduleResponse:
    try:
        loader = state.gtfs_loader

        response: list[TransitSchedule] = []

        if input.origin_station_id:
            response = loader.get_schedule(
                input.origin_station_id, input.destination_station_id).to_dict(orient="records")
        elif input.coordinates:
            # TODO: Implement reverse geocoding using coordinates
            pass
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
            next_schedules=response
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
