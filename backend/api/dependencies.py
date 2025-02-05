import base64
import hashlib
import hmac
import json
from operator import itemgetter
from typing import Annotated
from urllib.parse import parse_qsl

from config import BOT_TOKEN, TEST_MODE, TEST_USER
from database.models import User
from database.requests import get_user_by_id
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

auth_scheme = HTTPBearer()


async def get_current_user(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    decoded_bytes = base64.b64decode(token.credentials)
    decoded_string = decoded_bytes.decode('utf-8')

    user_data = validate_qsl_init_data(decoded_string)
    if not user_data:
        raise HTTPException(
            status_code=400, detail='Invalid auth data provided')

    user = await get_user_by_id(user_data.get('id'))
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    return user


def validate_qsl_init_data(init_data: str):
    initData: dict = dict(parse_qsl(init_data))
    return validate_init_data(init_data=initData)


def validate_init_data(init_data: dict):
    try:
        hash_ = init_data.pop('hash')
        data_check_string = "\n".join(
            f"{k}={v}" for k, v in sorted(init_data.items(), key=itemgetter(0))
        )
        secret_key = hmac.new(
            key=b"WebAppData", msg=BOT_TOKEN.encode(), digestmod=hashlib.sha256
        ).digest()
        calculated_hash = hmac.new(
            key=secret_key, msg=data_check_string.encode(), digestmod=hashlib.sha256
        ).hexdigest()
        if calculated_hash == hash_:
            user = json.loads(init_data['user'])
            del user['allows_write_to_pm']
            return user
    except Exception as e:
        pass

    return TEST_USER if TEST_MODE else None


WebAppUser = Annotated[User, Depends(get_current_user)]
