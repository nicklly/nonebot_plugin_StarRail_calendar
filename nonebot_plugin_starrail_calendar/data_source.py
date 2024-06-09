import json
import math
import os
import asyncio
import functools
import re
from datetime import datetime, timedelta
from pathlib import Path

from dateutil.relativedelta import relativedelta

from . import *

res = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'template')

# type 0 普通常驻任务深渊 1 新闻 2 蛋池 3 限时活动H5
event_data = {
    'cn': [],
}

event_updated = {
    'cn': '',
}

lock = {
    'cn': asyncio.Lock(),
}

ignored_key_words = [
    '有奖问卷',
    '公平运营',
    '防沉迷',
    '游戏优化',
    '保密测试',
    '社群',
    '社媒聚合页',
    '米游社',
    '阵容',
    '攻略征集',
    '激励',
    '角色PV',
    '版本PV',
    '角色演示'

]

ignored_ann_ids = [
    '194',
    '185',
    '318',
    '289',
    '350'
]
detail_api = 'https://hkrpg-api.mihoyo.com/common/hkrpg_cn/announcement/api/getAnnList?game=hkrpg&game_biz=hkrpg_cn&lang=zh-cn&auth_appid=announcement&authkey_ver=1&bundle_id=hkrpg_cn&channel_id=1&level=65&platform=pc&region=prod_gf_cn&sdk_presentation_style=fullscreen&sdk_screen_transparent=true&sign_type=2&uid=100000000'
# list_api = 'https://hkrpg-api.mihoyo.com/common/hkrpg_cn/announcement/api/getAnnList?game=hkrpg&game_biz=hkrpg_cn&lang=zh-cn&bundle_id=hkrpg_cn&platform=pc&region=prog_gf_cn&level=55&uid=100000000'
list_api = 'https://hkrpg-api.mihoyo.com/common/hkrpg_cn/announcement/api/getAnnContent?game=hkrpg&game_biz=hkrpg_cn&lang=zh-cn&bundle_id=hkrpg_cn&platform=pc&region=prod_gf_cn&level=55&uid=100000000'


def cache(ttl=timedelta(hours=1), arg_key=None):
    def wrap(func):
        cache_data = {}

        @functools.wraps(func)
        async def wrapped(*args, **kw):
            nonlocal cache_data
            default_data = {"time": None, "value": None}
            ins_key = 'default'
            if arg_key:
                ins_key = arg_key + str(kw.get(arg_key, ''))
                data = cache_data.get(ins_key, default_data)
            else:
                data = cache_data.get(ins_key, default_data)

            now = datetime.now()
            if not data['time'] or now - data['time'] > ttl:
                try:
                    data['value'] = await func(*args, **kw)
                    data['time'] = now
                    cache_data[ins_key] = data
                except Exception as e:
                    raise e

            return data['value']

        return wrapped

    return wrap


@cache(ttl=timedelta(hours=3), arg_key='url')
async def query_data(url):
    try:
        req = await get(url)
        return req.json()
    except:
        pass
    return None


async def load_event_cn():
    result = await utils.get(url=list_api)
    detail_result = await utils.get(url=detail_api)

    result = result.json()
    detail_result = detail_result.json()

    if result and 'retcode' in result and result['retcode'] == 0 and detail_result and 'retcode' in detail_result and \
            detail_result['retcode'] == 0:
        event_data['cn'] = []
        event_detail = {}

        for data in detail_result['data']['list'][0]['list']:
            event_detail[data['ann_id']] = data

            ignore = False
            for ann_id in ignored_ann_ids:
                if ann_id == data["ann_id"]:
                    ignore = True
                    break
            if ignore:
                continue

            for keyword in ignored_key_words:
                if keyword in data['title']:
                    ignore = True
                    break
            if ignore:
                continue

            start_time = datetime.strptime(data['start_time'], r"%Y-%m-%d %H:%M:%S")
            end_time = datetime.strptime(data['end_time'], r"%Y-%m-%d %H:%M:%S")

            # 从正文中查找开始时间
            if event_detail[data["ann_id"]]:
                content = event_detail[data["ann_id"]]['content']
                searchObj = re.search(
                    r'(\d+)\/(\d+)\/(\d+)\s(\d+):(\d+):(\d+)', content, re.M | re.I)
                try:
                    datelist = searchObj.groups()  # ('2021', '9', '17')
                    if datelist and len(datelist) >= 6:
                        ctime = datetime.strptime(
                            f'{datelist[0]}-{datelist[1]}-{datelist[2]} {datelist[3]}:{datelist[4]}:{datelist[5]}', r"%Y-%m-%d %H:%M:%S")
                        if start_time < ctime < end_time:
                            start_time = ctime
                except Exception as e:
                    pass

            event = {
                'title': data['title'],
                'banner': data['banner'],
                'color': '#2196f3',
                'type': 0,
                'start': start_time,
                'forever': False,
                'end': end_time
            }

            if re.search(r'(同行任务|新增关卡|开拓)', data['title']):
                event['color'] = '#2196f3'
                event['type'] = 1
                event['banner'] = data['banner']
                event['forever'] = True

            if '无名勋礼' in data['title']:
                event['color'] = '#F00078'
                event['type'] = 1
                event['forever'] = False
                event['banner'] = data['banner']

            if '位面分裂' in data['title']:
                event['type'] = 2
                event['forever'] = False
                event['color'] = '#E9AB17'
                event['banner'] = data['banner']

            event_data['cn'].append(event)

        # 光锥/角色活动跃迁
        for data2 in detail_result['data']['pic_list'][0]['type_list'][0]['list']:
            event_detail[data2['ann_id']] = data2

            start_time = datetime.strptime(data2['start_time'], r"%Y-%m-%d %H:%M:%S")
            end_time = datetime.strptime(data2['end_time'], r"%Y-%m-%d %H:%M:%S")

            # 从正文中查找开始时间
            if event_detail[data2["ann_id"]]:
                content = event_detail[data2["ann_id"]]['content']
                searchObj = re.search(
                    r'(\d+)\/(\d+)\/(\d+)\s(\d+):(\d+):(\d+)', content, re.M | re.I)
                try:
                    datelist = searchObj.groups()  # ('2021', '9', '17')
                    if datelist and len(datelist) >= 6:
                        ctime = datetime.strptime(
                            f'{datelist[0]}-{datelist[1]}-{datelist[2]} {datelist[3]}:{datelist[4]}:{datelist[5]}', r"%Y-%m-%d %H:%M:%S")
                        if start_time < ctime < end_time:
                            start_time = ctime
                except Exception as e:
                    pass

            event = {
                'title': data2['title'],
                'banner': data2['img'],
                'color': '#2196f3',
                'type': 0,
                'forever': False,
                'start': start_time,
                'end': end_time
            }

            if '活动跃迁' in data2['title']:
                event['type'] = 1
                event['forever'] = False
                event['color'] = '#73BF00'
                event['banner'] = data2['img']
            event_data['cn'].append(event)

        # 深渊提醒
        # i = 0
        # while i < 2:
        #     curmon = datetime.today() + relativedelta(months=i)
        #     nextmon = curmon + relativedelta(months=1)
        #     event_data['cn'].append({
        #         'title': '「忘却之庭·混沌回忆」· 上半段',
        #         'start': datetime.strptime(
        #             curmon.strftime("%Y/%m/01 04:00"), r"%Y/%m/%d %H:%M"),
        #         'end': datetime.strptime(
        #             curmon.strftime("%Y/%m/16 03:59"), r"%Y/%m/%d %H:%M"),
        #         'type': 0,
        #         'forever': False,
        #         'color': '#580dda',
        #         'banner': Path(__file__).parent / 'template' / 'sy.jpg'
        #     })
        #     event_data['cn'].append({
        #         'title': '「忘却之庭·混沌回忆」· 下半段 ',
        #         'start': datetime.strptime(
        #             curmon.strftime("%Y/%m/16 04:00"), r"%Y/%m/%d %H:%M"),
        #         'end': datetime.strptime(
        #             nextmon.strftime("%Y/%m/01 03:59"), r"%Y/%m/%d %H:%M"),
        #         'type': 0,
        #         'forever': False,
        #         'color': '#580dda',
        #         'banner': Path(__file__).parent / 'template' / 'sy.jpg'
        #     })
        #     i = i + 1
        return 0
    return 1


async def load_event(server):
    if server == 'cn':
        return await load_event_cn()
    return 1


async def get_events(server, offset, days):
    events = []
    pcr_now = datetime.now()
    if pcr_now.hour < 4:
        pcr_now -= timedelta(days=1)
    pcr_now = pcr_now.replace(
        hour=18, minute=0, second=0, microsecond=0)  # 用晚6点做基准

    await lock[server].acquire()
    try:
        t = pcr_now.strftime('%y%m%d')
        if event_updated[server] != t:
            if await load_event(server) == 0:
                event_updated[server] = t
    finally:
        lock[server].release()

    start = pcr_now + timedelta(days=offset)
    end = start + timedelta(days=days)
    end -= timedelta(hours=18)  # 晚上12点结束

    for event in event_data[server]:
        if end > event['start'] and start < event['end']:  # 在指定时间段内 已开始 且 未结束
            event['start_days'] = math.ceil((event['start'] - start) / timedelta(days=1))  # 还有几天开始
            event['left_days'] = math.floor((event['end'] - start) / timedelta(days=1))  # 还有几天结束
            events.append(event)


# 按type从大到小 按剩余天数从小到大
    events.sort(key=lambda item: item["type"] * 100 - item['left_days'], reverse=True)
    return events
