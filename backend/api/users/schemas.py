from common.schemas import BaseModel

class UserResponse(BaseModel):
    user_id: str | int
    username: str