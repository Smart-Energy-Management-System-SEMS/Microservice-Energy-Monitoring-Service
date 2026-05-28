from typing import List
from fastapi import APIRouter, Depends, HTTPException
from monitoring.application.commandservices.energy_meter_command_service import EnergyMeterCommandService
from monitoring.application.queryservices.energy_meter_query_service import EnergyMeterQueryService
from monitoring.domain.model.commands.register_energy_meter_command import RegisterEnergyMeterCommand
from monitoring.interfaces.rest.resources.energy_meter_resource import (
    RegisterEnergyMeterRequest, EnergyMeterResponse
)
from monitoring.interfaces.rest.transform.energy_meter_transform import EnergyMeterTransform
from monitoring.interfaces.rest.controllers.dependencies import (
    get_meter_command_service, get_meter_query_service
)

router = APIRouter(prefix="/energy-meters", tags=["Energy Meters"])


@router.post("", response_model=EnergyMeterResponse, status_code=201, summary="Register a new smart meter")
async def register_meter(
    request: RegisterEnergyMeterRequest,
    command_service: EnergyMeterCommandService = Depends(get_meter_command_service),
) -> EnergyMeterResponse:
    try:
        command = RegisterEnergyMeterCommand(
            user_id=request.user_id,
            meter_serial=request.meter_serial,
            model=request.model,
            brand=request.brand,
            location=request.location,
            firmware_version=request.firmware_version,
            max_power_watts=request.max_power_watts,
        )
        meter = await command_service.handle_register(command)
        return EnergyMeterTransform.to_response(meter)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/user/{user_id}", response_model=List[EnergyMeterResponse], summary="Get meters by user")
async def get_meters_by_user(
    user_id: str,
    query_service: EnergyMeterQueryService = Depends(get_meter_query_service),
) -> List[EnergyMeterResponse]:
    meters = await query_service.get_by_user(user_id)
    return [EnergyMeterTransform.to_response(m) for m in meters]


@router.patch("/{meter_id}/deactivate", response_model=EnergyMeterResponse, summary="Deactivate a meter")
async def deactivate_meter(
    meter_id: str,
    command_service: EnergyMeterCommandService = Depends(get_meter_command_service),
) -> EnergyMeterResponse:
    try:
        meter = await command_service.handle_deactivate(meter_id)
        return EnergyMeterTransform.to_response(meter)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{meter_id}", response_model=EnergyMeterResponse, summary="Get meter by ID")
async def get_meter_by_id(
    meter_id: str,
    query_service: EnergyMeterQueryService = Depends(get_meter_query_service),
) -> EnergyMeterResponse:
    meter = await query_service.get_by_id(meter_id)
    if not meter:
        raise HTTPException(status_code=404, detail=f"Meter '{meter_id}' not found")
    return EnergyMeterTransform.to_response(meter)
