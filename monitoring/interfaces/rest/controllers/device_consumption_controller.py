from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from monitoring.application.commandservices.device_consumption_command_service import DeviceConsumptionCommandService
from monitoring.application.queryservices.device_consumption_query_service import DeviceConsumptionQueryService
from monitoring.domain.model.commands.create_device_consumption_command import CreateDeviceConsumptionCommand
from monitoring.domain.model.queries.get_by_user_query import GetByUserQuery
from monitoring.domain.model.queries.get_by_device_query import GetByDeviceQuery
from monitoring.interfaces.rest.resources.device_consumption_resource import (
    CreateDeviceConsumptionRequest, DeviceConsumptionResponse
)
from monitoring.interfaces.rest.transform.device_consumption_transform import DeviceConsumptionTransform
from monitoring.interfaces.rest.controllers.dependencies import (
    get_consumption_command_service, get_consumption_query_service
)

router = APIRouter(prefix="/device-consumptions", tags=["Device Consumptions"])


@router.post("", response_model=DeviceConsumptionResponse, status_code=201, summary="Record device consumption")
async def create_device_consumption(
    request: CreateDeviceConsumptionRequest,
    command_service: DeviceConsumptionCommandService = Depends(get_consumption_command_service),
) -> DeviceConsumptionResponse:
    command = CreateDeviceConsumptionCommand(
        user_id=request.user_id,
        device_id=request.device_id,
        device_name=request.device_name,
        meter_id=request.meter_id,
        total_kwh=request.total_kwh,
        cost_estimate_soles=request.cost_estimate_soles,
        period_start=request.period_start,
        period_end=request.period_end,
        peak_power_watts=request.peak_power_watts,
        average_power_watts=request.average_power_watts,
        reading_count=request.reading_count,
    )
    consumption = await command_service.handle_create(command)
    return DeviceConsumptionTransform.to_response(consumption)


@router.get("/user/{user_id}", response_model=List[DeviceConsumptionResponse], summary="Get consumptions by user")
async def get_consumptions_by_user(
    user_id: str,
    limit: int = Query(default=50, ge=1, le=200),
    skip: int = Query(default=0, ge=0),
    query_service: DeviceConsumptionQueryService = Depends(get_consumption_query_service),
) -> List[DeviceConsumptionResponse]:
    items = await query_service.get_by_user(GetByUserQuery(user_id=user_id, limit=limit, skip=skip))
    return [DeviceConsumptionTransform.to_response(c) for c in items]


@router.get("/user/{user_id}/top", response_model=List[DeviceConsumptionResponse], summary="Top consuming devices")
async def get_top_consumers(
    user_id: str,
    limit: int = Query(default=5, ge=1, le=20),
    query_service: DeviceConsumptionQueryService = Depends(get_consumption_query_service),
) -> List[DeviceConsumptionResponse]:
    items = await query_service.get_top_consumers(user_id, limit)
    return [DeviceConsumptionTransform.to_response(c) for c in items]


@router.get("/{consumption_id}", response_model=DeviceConsumptionResponse, summary="Get consumption by ID")
async def get_consumption_by_id(
    consumption_id: str,
    query_service: DeviceConsumptionQueryService = Depends(get_consumption_query_service),
) -> DeviceConsumptionResponse:
    item = await query_service.get_by_id(consumption_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Consumption '{consumption_id}' not found")
    return DeviceConsumptionTransform.to_response(item)
