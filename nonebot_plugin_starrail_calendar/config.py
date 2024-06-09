from pydantic import BaseModel
from nonebot import get_driver


class PluginConfig(BaseModel):
    # 页面宽度
    width = 600
    # 页面高度
    height = 10
    # 浏览器内核
    browser_type = 'firefox'


config: PluginConfig = PluginConfig.parse_obj(get_driver().config.dict())
