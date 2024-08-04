from pydantic import BaseModel
from nonebot import get_driver


class PluginConfig(BaseModel):
    # 页面宽度
    width: int = 600
    # 页面高度
    height: int = 10
    # 浏览器内核
    browser_type: str = 'firefox'


config: PluginConfig = PluginConfig.parse_obj(get_driver().config.dict())
