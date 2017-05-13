# -*- coding: utf-8 -*-
# Copyright (c) 2017 YA-androidapp(https://github.com/YA-androidapp) All
# rights reserved.

import urllib.parse
import urllib.request
from datetime import datetime, timedelta
import math

from slackbot.bot import respond_to
from slackbot.bot import listen_to

today = datetime.today()

# 定数
station_last = "東京"  # 誤入力を防ぐために予め定数として保管しておく

# 処理


def get_norikae_url(ym, d, time, mode):
    return "http://www.jorudan.co.jp/norikae/cgi/nori.cgi?eki3=&via_on=1&Dym=" + \
        ym + "&Ddd=" + d + \
        "&Dhh=" + time[0:2] + "&Dmn1=" + time[2] + "&Dmn2=" + time[3] +\
        "&Cway=" + mode + "&Clate=1&Czu=2&C7=1&C2=0&C3=0&C1=0&C4=0&C6=2" + \
        "&S.x=3&S.y=2&Cmap1=&rf=nr&pg=0&eok1=&eok2=&eok3=&Csg=1&type=t&Cid=0&Cfp=1&"


@respond_to("電車")
@respond_to("経路")
@respond_to("乗換")
@listen_to("電車")
@listen_to("経路")
@listen_to("乗換")
def listen_norikae(message):
    station = message.body["text"] \
        .replace(r"@[^\s]+", "") \
        .replace("電車", "") \
        .replace("経路", "") \
        .replace("乗換", "") \
        .replace("　", " ") \
        .replace(r"[\r\n]+", " ")
    stations = station.strip().split(" ")
    station1 = ""
    station2 = ""
    time = ""

    if len(stations) == 3:
        station1 = stations[0]
        station2 = stations[1]
        time = stations[2].replace(":", "")
        message.send(norikae(station1, station2, get_norikae_url(
            today.strftime("%Y%m"), today.strftime("%d"), time, "0")))
    elif len(stations) == 2:
        station1 = stations[0]
        station2 = stations[1]
        time = (today + timedelta(minutes=12)).strftime("%H%M")
        message.send(norikae(station1, station2, get_norikae_url(
            today.strftime("%Y%m"), today.strftime("%d"), time, "0")))
    elif len(stations) == 1:
        station1 = stations[0]
        station2 = station_last
        time = (today + timedelta(minutes=12)).strftime("%H%M")
        message.send(norikae(station1, station2, get_norikae_url(
            today.strftime("%Y%m"), today.strftime("%d"), time, "0")))


@respond_to("終電")
@listen_to("終電")
def listen_last(message):
    station = message.body["text"] \
        .replace(r"@[^\s]+", "") \
        .replace("終電", "") \
        .replace(r"[[:blank:]]+", "")
    message.send(norikae(station, station_last, get_norikae_url(
        today.strftime("%Y%m"), today.strftime("%d"), "2300", "3")))


# 経路を検索する


def norikae(eki1, eki2, url):
    query = {
        "eki1": eki1,
        "eki2": eki2
    }
    req = urllib.parse.urlencode(query)
    res = urllib.request.urlopen(url + req)
    print(url + req)
    source = res.read().decode("utf-8")
    sources = source.split("<hr size=\"1\" color=\"black\" />")
    if len(sources) > 2:
        return sources[2]
    return ""
