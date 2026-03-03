"""API routes package."""
from src.routes.roles import router as roles_router
from src.routes.users import router as users_router
from src.routes.auth import router as auth_router
from src.routes.ws import router as ws_router
from src.routes.webhooks import router as webhooks_router

__all__ = ["roles_router", "users_router", "auth_router", "ws_router", "webhooks_router"]

