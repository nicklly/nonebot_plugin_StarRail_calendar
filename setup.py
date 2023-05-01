#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="nonebot_plugin_genshin_calendar",
    version="0.0.3",
    keywords=["pip", "nonebot_plugin_genshin_calendar"],
    description="查看原神活动日历",
    long_description="查看原神活动日历",
    license="GPL Licence",
    url="https://github.com/nicklly/nonebot_plugin_genshin_calendar",
    author="TonyKun",
    author_email="1134741727@qq.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        "Pillow >= 6.2.1",
        "nonebot2 >= 2.0.0b1",
        "nonebot-adapter-onebot >= 2.0.0b1",
    ],
)