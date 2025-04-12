from model.transit import TransitScheduleInput, TransitSchedule
import math


response: list[TransitSchedule] = [
    {
        "transit_mode": "rail",
        "eta_origin": "2025-04-12 16:19:09.383766",
        "eta_destination": "2025-04-12 17:19:09.383766"
    },
    {
        "transit_mode": "bus",
        "eta_origin": "2025-04-12 16:19:09.383766",
        "eta_destination": "2025-04-12 17:19:09.383766"
    },
    {
        "transit_mode": "light_rail",
        "eta_origin": "2025-04-12 16:19:09.383766",
        "eta_destination": "2025-04-12 17:19:09.383766"
    },
]


def get_next_transit_schedules(state: any, input: TransitScheduleInput, page: int = 1, limit: int = 10):
    try:
        # get total number of schedules
        total_schedules = len(response)
        total_pages = math.ceil(total_schedules / limit)
        skip = (page - 1) * limit

        print(total_schedules, total_pages, skip,
              limit, response)

        return {
            "total_schedules": total_schedules,
            "total_pages": total_pages,
            "current_page": page,
            "next_schedules": response[skip:skip + limit]
        }

    except Exception as e:
        return {"error": "Error getting transit schedule", "message": str(e)}
