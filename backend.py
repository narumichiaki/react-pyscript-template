from typing import Any
import sys
import logging
import js
from pydantic import BaseModel, field_validator
from backend_helper import APP, Response, api_endpoint

logging.basicConfig(stream = sys.stdout)
LOGGER: logging.Logger = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


### MODEL ###



### CONTROLLER ###



### API ###
# サンプル： パラメータのバリデーションあり
class Message(BaseModel):
    message: str
    @field_validator('message', mode = 'before')
    @classmethod
    def convert_to_string(cls, v):
        return str(v)
@APP.route("/log", Message)
def log(message: Message):
    response_message: str = f"/log: Recieved log message: {message.message}"
    LOGGER.info(response_message)
    return Response.ok({"message": response_message})

# サンプル： パラメータのバリデーションなし
@APP.route("/log_unsafe")
def log_unsafe(message: dict[str, str]):
    response_message: str = f"/log_unsafe: Recieved log message: {message["message"]}"
    LOGGER.info(response_message)
    return Response.ok({"message": response_message})


# APIエンドポイントをwindowに登録(必須)
js.window.api_endpoint = api_endpoint