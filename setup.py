#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="nonebot_plugin_star_rail_calendar",
    version="0.0.1",
    keywords=["pip", "nonebot_plugin_star_rail_calendar"],
    description="查看《崩坏：星穹铁道》官方活动",
    long_description="查看《崩坏：星穹铁道》官方活动",
    license="GPL Licence",
    url="https://github.com/nicklly/nonebot_plugin_star_rail_calendar",
    author="TonyKun",
    author_email="1134741727@qq.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        "nonebot2 >= 2.0.0b1",
        "nonebot-adapter-onebot >= 2.0.0b1",
    ],
)