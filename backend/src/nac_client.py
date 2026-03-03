"""Network as Code client initialization."""
import network_as_code as nac
from network_as_code.models.geofencing import EventType, Circle, Center
from typing import Dict
from src.config import settings
from src.logging_config import get_logger

logger = get_logger(__name__)

# Global NAC client instance
_nac_client = None

# Global devices storage
_devices: Dict[str, nac.Device] = {}

# Phone numbers for devices
PHONE_NUMBERS = [
    "+36729991000",
    "+36729991001",
    "+36709991002",
    "+36709991003",
    "+34640197348"
    #"+36709991004",
    #"+36379991005",
    # "+36729991006",
    # "+36379991007",
    # "+999991234567",
]

# Geofencing area configuration
GEOFENCING_CENTER_LATITUDE = 41.373147
GEOFENCING_CENTER_LONGITUDE = 2.149031
GEOFENCING_RADIUS = 200  # meters

# Webhook URL for geofencing notifications
GEOFENCING_WEBHOOK_URL = "https://a220-95-215-123-97.ngrok-free.app/webhooks/geofencing"

# Global subscriptions storage
_subscriptions: Dict[str, nac.Subscription] = {}


def get_nac_client() -> nac.NetworkAsCodeClient:
    """
    Get or create NAC client instance.

    Returns:
        nac.NetworkAsCodeClient: Initialized Network as Code client
    """
    global _nac_client

    if _nac_client is None:
        try:
            _nac_client = nac.NetworkAsCodeClient(
                token=settings.nac_token,
            )
            logger.info("nac_client_initialized")
        except Exception as e:
            logger.error("nac_client_initialization_failed", error=str(e))
            raise

    return _nac_client


def initialize_devices() -> Dict[str, nac.Device]:
    """
    Initialize and cache device objects from phone numbers.

    Returns:
        Dict[str, nac.Device]: Dictionary of phone_number -> device
    """
    global _devices

    if _devices:
        logger.info("devices_already_initialized", count=len(_devices))
        return _devices

    try:
        client = get_nac_client()

        for phone_number in PHONE_NUMBERS:
            try:
                device = client.devices.get(
                    phone_number=phone_number,
                )
                _devices[phone_number] = device
                logger.info("device_initialized", phone_number=phone_number)
            except Exception as e:
                logger.error(
                    "device_initialization_failed",
                    phone_number=phone_number,
                    error=str(e),
                )

        logger.info("devices_initialization_complete", count=len(_devices))
        return _devices

    except Exception as e:
        logger.error("devices_initialization_failed", error=str(e))
        raise


def get_devices() -> Dict[str, nac.Device]:
    """Get cached devices."""
    return _devices


def get_device(phone_number: str) -> nac.Device:
    """
    Get device by phone number.

    Args:
        phone_number: Phone number of the device

    Returns:
        nac.Device: Device object

    Raises:
        KeyError: If device not found
    """
    if phone_number not in _devices:
        raise KeyError(f"Device not found for phone number: {phone_number}")

    return _devices[phone_number]


def subscribe_to_geofencing() -> Dict[str, nac.Subscription]:
    """
    Subscribe all devices to geofencing notifications.

    Creates geofencing subscriptions for all initialized devices.
    Triggers AREA_LEFT events when device leaves the defined area.

    Returns:
        Dict[str, nac.Subscription]: Dictionary of phone_number -> subscription
    """
    global _subscriptions

    if _subscriptions:
        logger.info("geofencing_subscriptions_already_created", count=len(_subscriptions))
        return _subscriptions

    try:
        client = get_nac_client()

        # Create geofencing area
        area = Circle(
            center=Center(
                latitude=GEOFENCING_CENTER_LATITUDE,
                longitude=GEOFENCING_CENTER_LONGITUDE,
            ),
            radius=GEOFENCING_RADIUS,
        )

        # Subscribe each device to geofencing
        for phone_number, device in _devices.items():
            try:
                subscription = client.geofencing.subscribe(
                    device=device,
                    sink=GEOFENCING_WEBHOOK_URL,
                    types=[EventType.AREA_LEFT],
                    area=area,
                )
                _subscriptions[phone_number] = subscription
                logger.info(
                    "geofencing_subscription_created",
                    phone_number=phone_number,
                    latitude=GEOFENCING_CENTER_LATITUDE,
                    longitude=GEOFENCING_CENTER_LONGITUDE,
                    radius=GEOFENCING_RADIUS,
                )
            except Exception as e:
                logger.error(
                    "geofencing_subscription_failed",
                    phone_number=phone_number,
                    error=str(e),
                )

        logger.info("geofencing_subscriptions_complete", count=len(_subscriptions))
        return _subscriptions

    except Exception as e:
        logger.error("geofencing_subscriptions_failed", error=str(e))
        raise


def get_subscriptions() -> Dict[str, nac.Subscription]:
    """Get all geofencing subscriptions."""
    return _subscriptions

