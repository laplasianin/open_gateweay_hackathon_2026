"""WebSocket endpoints for real-time data."""
import asyncio
from datetime import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.markers import get_current_markers, update_markers_with_variation
from src.models import MarkersUpdate, DeviceLocationsUpdate, DeviceLocation
from src.nac_client import get_devices
from src.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/ws",
    tags=["websocket"],
)


@router.websocket("/markers")
async def websocket_markers(websocket: WebSocket):
    """
    WebSocket endpoint for real-time markers updates.
    
    Sends markers every 15 seconds.
    Updates marker coordinates every 10 seconds with small variations.
    """
    await websocket.accept()
    logger.info("websocket_markers_connected")
    
    update_counter = 0
    
    try:
        while True:
            # Update markers every 10 seconds (2 cycles of 5 seconds)
            if update_counter % 2 == 0:
                update_markers_with_variation()
                logger.info("markers_updated_with_variation")
            
            # Get current markers
            markers = get_current_markers()
            
            # Create update message
            update = MarkersUpdate(
                markers=markers,
                timestamp=datetime.utcnow(),
            )
            
            # Send to client
            await websocket.send_json(update.model_dump(mode="json"))
            logger.info("markers_sent_to_client", count=len(markers))
            
            # Wait 5 seconds before next send
            # (3 sends = 15 seconds total)
            await asyncio.sleep(5)
            update_counter += 1
            
    except WebSocketDisconnect:
        logger.info("websocket_markers_disconnected")
    except Exception as e:
        logger.error("websocket_markers_error", error=str(e))
        await websocket.close(code=1011)


@router.websocket("/markers_real")
async def websocket_markers_real(websocket: WebSocket):
    """
    WebSocket endpoint for real-time device locations from NAC.

    Queries all devices every 15 seconds using NAC location API.
    Returns actual device coordinates from the operator.
    """
    await websocket.accept()
    logger.info("websocket_markers_real_connected")

    try:
        while True:
            devices = get_devices()

            if not devices:
                logger.warning("no_devices_available")
                await asyncio.sleep(15)
                continue

            device_locations = []

            # Query location for each device
            for phone_number, device in devices.items():
                try:
                    location_data = device.location(max_age=60)

                    # Parse location response (NAC Location object)
                    device_loc = DeviceLocation(
                        phone_number=phone_number,
                        longitude=location_data.longitude,
                        latitude=location_data.latitude,
                        radius=location_data.radius,
                    )
                    device_locations.append(device_loc)
                    logger.info(
                        "device_location_queried",
                        phone_number=phone_number,
                        latitude=location_data.latitude,
                        longitude=location_data.longitude,
                        radius=location_data.radius,
                    )

                except Exception as e:
                    logger.error(
                        "device_location_query_failed",
                        phone_number=phone_number,
                        error=str(e),
                    )

            # Create update message
            update = DeviceLocationsUpdate(
                devices=device_locations,
                timestamp=datetime.utcnow(),
            )

            # Send to client
            await websocket.send_json(update.model_dump(mode="json"))
            logger.info("device_locations_sent_to_client", count=len(device_locations))

            # Wait 15 seconds before next query
            await asyncio.sleep(15)

    except WebSocketDisconnect:
        logger.info("websocket_markers_real_disconnected")
    except Exception as e:
        logger.error("websocket_markers_real_error", error=str(e))
        await websocket.close(code=1011)

