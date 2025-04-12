from fastapi import APIRouter, Request
from transit import get_next_transit_schedules
from model import TransitScheduleInput, TransitScheduleResponse

router = APIRouter()


@router.get("/", response_model=dict)
async def root():
    return {"message": "Hello World"}


@router.post("/api/v1/transit/schedules", response_model=TransitScheduleResponse)
async def get_transit_schedules(request: Request, input: TransitScheduleInput, page: int = 1, limit: int = 1):
    return get_next_transit_schedules(request.app.state, input, page, limit)
