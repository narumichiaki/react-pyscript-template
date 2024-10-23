from typing import Callable, Any
import sys
import logging
import js
import json
from pydantic import BaseModel, field_validator

logging.basicConfig(stream = sys.stdout)
LOGGER: logging.Logger = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


### MODEL ###



### CONTROLLER = API ###
# API Router
class Router:
    def __init__(self):
        self.routes: dict[str, tuple[Callable, type[BaseModel]]] = {}

    def route(self, path: str, model: type[BaseModel]) -> Any:
        def decorator(func: Callable):
            # パス、メソッド、関数、およびPydanticモデルを登録
            self.routes[path] = (func, model)
            return func
        return decorator

    def call_route(self, path: str, json: dict) -> Any:
        route_info = self.routes.get(path)
        if route_info:
            route_func, model = route_info
            # Pydanticモデルでデータをバリデーションおよびパース
            data = model(**json)
            return route_func(data)
        else:
            raise ValueError(f"Route {path} not found.")
APP = Router()


# サンプルAPI
class Message(BaseModel):
    message: str
    @field_validator('message', mode = 'before')
    @classmethod
    def convert_to_string(cls, v):
        return str(v)

@APP.route("/log", Message)
def log(message: Message):
    LOGGER.info(message.message)
    return {"message": message.message}


# エンドポイント
def api_endpoint(path: str, json_param: str) -> str:
    data: Any = json.loads(json_param)
    response: dict = APP.call_route(path, data)
    return json.dumps(response)

# APIエンドポイントをwindowに登録(必須)
js.window.api_endpoint = api_endpoint