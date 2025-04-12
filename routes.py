from fastapi import APIRouter, Request
from service.transit import get_next_transit_schedules
from model.transit import TransitScheduleInput

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.post("/api/v1/transit/schedules")
async def get_transit_schedules(request: Request, input: TransitScheduleInput, page: int = 1, limit: int = 1):
    return get_next_transit_schedules(request.app.state, input, page, limit)
