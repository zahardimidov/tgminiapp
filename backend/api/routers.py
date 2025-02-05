from fastapi import APIRouter
from fastapi.routing import APIRoute
from api.users import router as users_router

router = APIRouter(prefix='')
router.include_router(users_router)


for route in router.routes:
    if isinstance(route, APIRoute):
        route.response_model_exclude_none = True
        parts = route.path.lstrip('/').split('/')
        route.operation_id = (parts[0] + ''.join(part.capitalize() for part in parts[1:])).replace('-', '')

