from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from monitoring.application.commandservices.consumption_alert_command_service import ConsumptionAlertCommandService
from monitoring.application.queryservices.consumption_alert_query_service import ConsumptionAlertQueryService
from monitoring.domain.model.commands.create_consumption_alert_command import CreateConsumptionAlertCommand
from monitoring.domain.model.queries.get_by_user_query import GetByUserQuery
from monitoring.interfaces.rest.resources.consumption_alert_resource import (
    CreateConsumptionAlertRequest, ConsumptionAlertResponse
)
from monitoring.interfaces.rest.transform.consumption_alert_transform import ConsumptionAlertTransform
from monitoring.interfaces.rest.controllers.dependencies import (
    get_alert_command_service, get_alert_query_service
)

router = APIRouter(prefix="/consumption-alerts", tags=["Consumption Alerts"])


@router.post("", response_model=ConsumptionAlertResponse, status_code=201, summary="Create a consumption alert")
async def create_alert(
    request: CreateConsumptionAlertRequest,
    command_service: ConsumptionAlertCommandService = Depends(get_alert_command_service),
) -> ConsumptionAlertResponse:
    command = CreateConsumptionAlertCommand(
        user_id=request.user_id,
        device_id=request.device_id,
        meter_id=request.meter_id,
        alert_type=request.alert_type,
        severity=request.severity,
        threshold_value=request.threshold_value,
        actual_value=request.actual_value,
        message=request.message,
    )
    alert = await command_service.handle_create(command)
    return ConsumptionAlertTransform.to_response(alert)


@router.get("/user/{user_id}", response_model=List[ConsumptionAlertResponse], summary="Get alerts by user")
async def get_alerts_by_user(
    user_id: str,
    limit: int = Query(default=50, ge=1, le=200),
    skip: int = Query(default=0, ge=0),
    query_service: ConsumptionAlertQueryService = Depends(get_alert_query_service),
) -> List[ConsumptionAlertResponse]:
    alerts = await query_service.get_by_user(GetByUserQuery(user_id=user_id, limit=limit, skip=skip))
    return [ConsumptionAlertTransform.to_response(a) for a in alerts]


@router.get("/user/{user_id}/unread", response_model=List[ConsumptionAlertResponse], summary="Get unread alerts")
async def get_unread_alerts(
    user_id: str,
    query_service: ConsumptionAlertQueryService = Depends(get_alert_query_service),
) -> List[ConsumptionAlertResponse]:
    alerts = await query_service.get_unread_by_user(user_id)
    return [ConsumptionAlertTransform.to_response(a) for a in alerts]


@router.patch("/{alert_id}/read", response_model=ConsumptionAlertResponse, summary="Mark alert as read")
async def mark_alert_as_read(
    alert_id: str,
    command_service: ConsumptionAlertCommandService = Depends(get_alert_command_service),
) -> ConsumptionAlertResponse:
    try:
        alert = await command_service.handle_mark_as_read(alert_id)
        return ConsumptionAlertTransform.to_response(alert)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{alert_id}/resolve", response_model=ConsumptionAlertResponse, summary="Resolve an alert")
async def resolve_alert(
    alert_id: str,
    command_service: ConsumptionAlertCommandService = Depends(get_alert_command_service),
) -> ConsumptionAlertResponse:
    try:
        alert = await command_service.handle_resolve(alert_id)
        return ConsumptionAlertTransform.to_response(alert)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{alert_id}", response_model=ConsumptionAlertResponse, summary="Get alert by ID")
async def get_alert_by_id(
    alert_id: str,
    query_service: ConsumptionAlertQueryService = Depends(get_alert_query_service),
) -> ConsumptionAlertResponse:
    alert = await query_service.get_by_id(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail=f"Alert '{alert_id}' not found")
    return ConsumptionAlertTransform.to_response(alert)
