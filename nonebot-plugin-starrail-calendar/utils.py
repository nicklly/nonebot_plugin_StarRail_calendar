import json
import httpx
from pathlib import Path
from typing import Dict, Optional, Any, Union


def load_data(data_file):
    data_path = Path() / 'data' / 'star_rali_calendar' / data_file
    if not data_path.exists():
        save_data({}, data_file)
    return json.load(data_path.open('r', encoding='utf-8'))


def save_data(data, data_file):
    data_path = Path() / 'data' / 'star_rali_calendar' / data_file
    data_path.parent.mkdir(parents=True, exist_ok=True)
    json.dump(data, data_path.open('w', encoding='utf-8'), ensure_ascii=False, indent=2)


async def get(url: str,
              *,
              headers: Optional[Dict[str, str]] = None,
              params: Optional[Dict[str, Any]] = None,
              timeout: Optional[int] = 20,
              **kwargs) -> httpx.Response:
    """
    说明：
        httpx的get请求封装
    参数：
        :param url: url
        :param headers: 请求头
        :param params: params
        :param timeout: 超时时间
    """
    async with httpx.AsyncClient() as client:
        return await client.get(url,
                                headers=headers,
                                params=params,
                                timeout=timeout,
                                **kwargs)


async def post(url: str,
               *,
               headers: Optional[Dict[str, str]] = None,
               params: Optional[Dict[str, Any]] = None,
               data: Optional[Dict[str, Any]] = None,
               json: Optional[Dict[str, Union[Any, str]]] = None,
               timeout: Optional[int] = 20,
               **kwargs) -> httpx.Response:
    """
    说明：
        httpx的post请求封装
    参数：
        :param url: url
        :param headers: 请求头
        :param params: params
        :param data: data
        :param json: json
        :param timeout: 超时时间
    """
    async with httpx.AsyncClient() as client:
        return await client.post(url,
                                 headers=headers,
                                 params=params,
                                 data=data,
                                 json=json,
                                 timeout=timeout,
                                 **kwargs)
