import jwt
from typing import Dict
import uuid6


def decode_safely(token: str, secret: str = "ERP@3@5@5") -> None | Dict[str, str]:
    try:
        jwt_data = jwt.decode(token, secret, algorithms=["HS256"])
        return jwt_data
    except jwt.PyJWTError:
        return None


def encode_safely(uuid: str, secret: str = "ERP@3@5@5"):
    jwt_token = jwt.encode({"uuid": str(uuid)}, secret, algorithm="HS256")
    return jwt_token
