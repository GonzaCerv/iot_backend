from fastapi.routing import APIRouter

from iot_web.web.api import echo, monitoring, user
from iot_web.db.dependencies import get_db_session

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(user.router, prefix="/users", tags=["users"])
