from typing import Callable, Any
from dataclasses import dataclass
import sys
import logging
import json
from pydantic import BaseModel

logging.basicConfig(stream = sys.stdout)
LOGGER: logging.Logger = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


# API Router（APIをデコレータで表現できるようにしつつ、バグ予防のためにAPIから受け取る値をチェックする）
class Router:
    def __init__(self):
        self.routes: dict[str, tuple[Callable, type[BaseModel] | None]] = {}

    def route(self, path: str, model: type[BaseModel] | None = None) -> Any:
        def decorator(func: Callable):
            # パス、メソッド、関数、およびPydanticモデルを登録
            self.routes[path] = (func, model)
            return func
        return decorator

    def call_route(self, path: str, json_param: dict[str, Any]) -> Any:
        route_info = self.routes.get(path)
        if route_info:
            route_func, model = route_info
            # Pydanticを用いて入力をチェック
            if model:
                try:
                    data = model(**json_param)
                    return route_func(data)
                except ValueError as e:
                    return Response.bad_request(f"入力データのフォーマットがAPI\"{path}\"の仕様と整合しません。： {str(e)}")
            else:
                return route_func(json_param)
        else:
            return Response.bad_request(f"指定されたパス\"{path}\"が見つかりません。")
APP = Router()


# レスポンスを表すクラス
@dataclass
class Response:
    status_code: int
    content: dict[str, Any]

    @classmethod
    def ok(cls, content: dict[str, Any]):
        return cls(200, content)
    
    @classmethod
    def bad_request(cls, error_message: str):
        return cls(400, { "error": "Bad Request. " + error_message })

    @classmethod
    def error(cls, error_message: str):
        return cls(500, { "error": "Internal Server Error. " + error_message })

    def to_return(self):
        return (str(self.status_code), json.dumps(self.content, ensure_ascii = False))


# エンドポイント
def api_endpoint(path: str, json_param: str) -> str:
    response: Response
    try:
        data: dict[str, Any] = json.loads(json_param)
        response = APP.call_route(path, data)
    except json.JSONDecodeError as e:
        LOGGER.fatal(f"JSONデコードエラー： {e}")
        response = Response.bad_request(f"無効なJSON形式です： {str(e)}")
    except Exception as e:
        LOGGER.fatal(f"予期せぬエラーが発生しました： {e}")
        response = Response.error(str(e))
    return response.to_return()
