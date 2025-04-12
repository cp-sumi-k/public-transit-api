from model.transit import TransitScheduleInput, TransitSchedule
import math


def get_next_transit_schedules(state: any, input: TransitScheduleInput, page: int = 1, limit: int = 10):
    try:
        loader = state.gtfs_loader

        response = []

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

        return {
            "total_schedules": total_schedules,
            "total_pages": total_pages,
            "current_page": page,
            "next_schedules": response[skip:skip + limit]
        }

    except Exception as e:
        return {"error": "Error getting transit schedule", "message": str(e)}
