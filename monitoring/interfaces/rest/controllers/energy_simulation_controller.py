from fastapi import APIRouter, Depends, HTTPException, Query

from monitoring.application.commandservices.energy_simulation_command_service import EnergySimulationCommandService
from monitoring.application.queryservices.energy_simulation_query_service import EnergySimulationQueryService
from monitoring.interfaces.rest.controllers.dependencies import (
    get_energy_simulation_command_service,
    get_energy_simulation_query_service,
)
from monitoring.interfaces.rest.resources.energy_simulation_resource import (
    ConsumptionHistoryResponse,
    CurrentConsumptionResponse,
    EnergyPricingResponse,
    SimulateEnergyReadingRequest,
    SimulatedEnergyReadingResponse,
)
from monitoring.interfaces.rest.transform.energy_simulation_transform import EnergySimulationTransform

router = APIRouter(prefix="/energy", tags=["Energy Simulation"])


@router.post("/simulation/readings", response_model=SimulatedEnergyReadingResponse, status_code=201)
async def generate_simulated_reading(
    request: SimulateEnergyReadingRequest,
    command_service: EnergySimulationCommandService = Depends(get_energy_simulation_command_service),
) -> SimulatedEnergyReadingResponse:
    reading, price, estimated_cost = await command_service.generate_reading(
        user_id=request.user_id,
        device_id=request.device_id,
        device_type=request.device_type,
    )
    return EnergySimulationTransform.to_reading_response(reading, price, estimated_cost)


@router.get("/devices/{device_id}/consumption/current", response_model=CurrentConsumptionResponse)
async def get_current_consumption(
    device_id: str,
    query_service: EnergySimulationQueryService = Depends(get_energy_simulation_query_service),
) -> CurrentConsumptionResponse:
    current = await query_service.get_current_consumption(device_id)
    if not current:
        raise HTTPException(status_code=404, detail=f"No readings found for device '{device_id}'")
    reading, price, estimated_cost = current
    return EnergySimulationTransform.to_current_response(reading, price, estimated_cost)


@router.get("/devices/{device_id}/consumption/history", response_model=ConsumptionHistoryResponse)
async def get_consumption_history(
    device_id: str,
    limit: int = Query(default=50, ge=1, le=200),
    skip: int = Query(default=0, ge=0),
    query_service: EnergySimulationQueryService = Depends(get_energy_simulation_query_service),
) -> ConsumptionHistoryResponse:
    items = await query_service.get_consumption_history(device_id, limit=limit, skip=skip)
    return ConsumptionHistoryResponse(
        device_id=device_id,
        records=[
            EnergySimulationTransform.to_reading_response(reading, price, estimated_cost)
            for reading, estimated_cost, price in items
        ],
    )


@router.get("/pricing/current", response_model=EnergyPricingResponse)
async def get_current_pricing(
    query_service: EnergySimulationQueryService = Depends(get_energy_simulation_query_service),
) -> EnergyPricingResponse:
    price = await query_service.get_current_price()
    return EnergySimulationTransform.to_pricing_response(price)
