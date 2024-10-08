import hashlib
import hmac
import json
from operator import itemgetter
from urllib.parse import parse_qsl

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from config import BOT_TOKEN, WEBHOOK_PATH
from database.requests import get_user
from database.schemas import WebAppRequest


def webapp_user_middleware(func):
    async def wrapper(request: Request):
        if str(request.url).endswith(WEBHOOK_PATH) or request.method == 'GET':
            return await func(request)

        body = await request.body()
        data: dict = json.loads(body.decode())
        init_data = data.get('data')

        error_text = 'Open this page from telegram'

        try:
            parsed_data = dict(parse_qsl(init_data))
        except ValueError:
            return HTTPException(status_code=401, detail=error_text)
        if "hash" not in parsed_data:
            return HTTPException(status_code=401, detail=error_text)

        hash_ = parsed_data.pop('hash')
        data_check_string = "\n".join(
            f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
        )
        secret_key = hmac.new(
            key=b"WebAppData", msg=BOT_TOKEN.encode(), digestmod=hashlib.sha256
        ).digest()
        calculated_hash = hmac.new(
            key=secret_key, msg=data_check_string.encode(), digestmod=hashlib.sha256
        ).hexdigest()
        if calculated_hash == hash_:
            user_data = json.loads(parsed_data['user'])

            user = await get_user(user_id=user_data['id'])

            webapp_request = WebAppRequest(
                webapp_user=user, **request.__dict__)

            return await func(webapp_request)
        return HTTPException(status_code=401, detail=error_text)

    return wrapper
