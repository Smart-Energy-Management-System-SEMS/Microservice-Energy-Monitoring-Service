from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from monitoring.application.commandservices.energy_reading_command_service import EnergyReadingCommandService
from monitoring.application.queryservices.energy_reading_query_service import EnergyReadingQueryService
from monitoring.domain.model.commands.create_energy_reading_command import CreateEnergyReadingCommand
from monitoring.domain.model.queries.get_by_user_query import GetByUserQuery
from monitoring.domain.model.queries.get_by_device_query import GetByDeviceQuery
from monitoring.domain.model.queries.get_by_date_range_query import GetByDateRangeQuery
from monitoring.interfaces.rest.resources.energy_reading_resource import (
    CreateEnergyReadingRequest, EnergyReadingResponse
)
from monitoring.interfaces.rest.transform.energy_reading_transform import EnergyReadingTransform
from monitoring.interfaces.rest.controllers.dependencies import (
    get_reading_command_service, get_reading_query_service
)

router = APIRouter(prefix="/energy-readings", tags=["Energy Readings"])


@router.post("", response_model=EnergyReadingResponse, status_code=201, summary="Record a new energy reading")
async def create_energy_reading(
    request: CreateEnergyReadingRequest,
    command_service: EnergyReadingCommandService = Depends(get_reading_command_service),
) -> EnergyReadingResponse:
    command = CreateEnergyReadingCommand(
        user_id=request.user_id,
        meter_id=request.meter_id,
        device_id=request.device_id,
        power_watts=request.power_watts,
        voltage=request.voltage,
        current=request.current,
        frequency=request.frequency,
        energy_kwh=request.energy_kwh,
        timestamp=request.timestamp,
        reading_type=request.reading_type,
        phase=request.phase,
    )
    reading = await command_service.handle_create(command)
    return EnergyReadingTransform.to_response(reading)


@router.get("/user/{user_id}", response_model=List[EnergyReadingResponse], summary="Get readings by user")
async def get_readings_by_user(
    user_id: str,
    limit: int = Query(default=50, ge=1, le=200),
    skip: int = Query(default=0, ge=0),
    query_service: EnergyReadingQueryService = Depends(get_reading_query_service),
) -> List[EnergyReadingResponse]:
    readings = await query_service.get_by_user(GetByUserQuery(user_id=user_id, limit=limit, skip=skip))
    return [EnergyReadingTransform.to_response(r) for r in readings]


@router.get("/device/{device_id}", response_model=List[EnergyReadingResponse], summary="Get readings by device")
async def get_readings_by_device(
    device_id: str,
    user_id: str = Query(..., description="Owner user ID"),
    limit: int = Query(default=50, ge=1, le=200),
    skip: int = Query(default=0, ge=0),
    query_service: EnergyReadingQueryService = Depends(get_reading_query_service),
) -> List[EnergyReadingResponse]:
    readings = await query_service.get_by_device(
        GetByDeviceQuery(device_id=device_id, user_id=user_id, limit=limit, skip=skip)
    )
    return [EnergyReadingTransform.to_response(r) for r in readings]


@router.get("/range", response_model=List[EnergyReadingResponse], summary="Get readings by date range")
async def get_readings_by_date_range(
    user_id: str = Query(...),
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    device_id: Optional[str] = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    query_service: EnergyReadingQueryService = Depends(get_reading_query_service),
) -> List[EnergyReadingResponse]:
    readings = await query_service.get_by_date_range(
        GetByDateRangeQuery(user_id=user_id, start_date=start_date, end_date=end_date,
                            device_id=device_id, limit=limit)
    )
    return [EnergyReadingTransform.to_response(r) for r in readings]


@router.get("/meter/{meter_id}/latest", response_model=EnergyReadingResponse, summary="Get latest reading by meter")
async def get_latest_by_meter(
    meter_id: str,
    query_service: EnergyReadingQueryService = Depends(get_reading_query_service),
) -> EnergyReadingResponse:
    reading = await query_service.get_latest_by_meter(meter_id)
    if not reading:
        raise HTTPException(status_code=404, detail=f"No readings found for meter '{meter_id}'")
    return EnergyReadingTransform.to_response(reading)


@router.get("/{reading_id}", response_model=EnergyReadingResponse, summary="Get reading by ID")
async def get_reading_by_id(
    reading_id: str,
    query_service: EnergyReadingQueryService = Depends(get_reading_query_service),
) -> EnergyReadingResponse:
    reading = await query_service.get_by_id(reading_id)
    if not reading:
        raise HTTPException(status_code=404, detail=f"Reading '{reading_id}' not found")
    return EnergyReadingTransform.to_response(reading)
