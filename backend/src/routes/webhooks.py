"""Webhook endpoints for receiving notifications."""
from fastapi import APIRouter, Request
from src.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/webhooks",
    tags=["webhooks"],
)


@router.post("/geofencing")
async def geofencing_webhook(request: Request):
    """
    Webhook endpoint for receiving geofencing notifications.
    
    Receives CloudEvents notifications when devices leave geofenced areas.
    Logs the incoming JSON payload for debugging and monitoring.
    
    Returns:
        dict: Acknowledgment response
    """
    try:
        # Get raw JSON body
        body = await request.json()
        print(body)
        logger.info(
            "geofencing_webhook_received",
            event_id=body.get("id"),
            event_type=body.get("type"),
            source=body.get("source"),
            time=body.get("time"),
        )
        
        # Log full payload for debugging
        logger.debug("geofencing_webhook_payload", payload=body)
        
        # Extract device and area info if available
        data = body.get("data", {})
        if data:
            logger.info(
                "geofencing_event_data",
                subscription_id=data.get("subscriptionId"),
                device=data.get("device"),
                area=data.get("area"),
            )
        
        return {
            "status": "received",
            "event_id": body.get("id"),
        }
        
    except Exception as e:
        logger.error("geofencing_webhook_error", error=str(e))
        return {
            "status": "error",
            "error": str(e),
        }

