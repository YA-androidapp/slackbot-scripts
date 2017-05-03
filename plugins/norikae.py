# -*- coding: utf-8 -*-
# Copyright (c) 2017 YA-androidapp(https://github.com/YA-androidapp) All
# rights reserved.

import urllib.parse
import urllib.request
import datetime

from slackbot.bot import respond_to
from slackbot.bot import listen_to

today = datetime.datetime.today()

# 定数
url_norikae = "http://www.jorudan.co.jp/norikae/cgi/nori.cgi?Sok=%E6%B1%BA+%E5%AE%9A&eok1=R-&eok2=R-&eki3=&eok3=&eki4=&eok4=&eki5=&eok5=&eki6=&eok6=&rf=nr&pg=0&Dym=" + \
    today.strftime("%Y%m") + \
    "&Ddd=" + today.strftime("%d") +\
    "&Dhh=0&Dmn=0&Cway=3&C1=0&C2=0&C3=0&C4=0&C6=2&Cmap1=&Czu=2&Clate=1&type=t&Cid=1&Cfp=1&"

eki2 = "東京"  # 誤入力を防ぐために予め定数として保管しておく

# 処理


@respond_to("終電")
@listen_to("終電")
def listen_norikae(message):
    station = message.body["text"] \
        .replace(r"@[^\s]+", "") \
        .replace("終電", "") \
        .replace(r"[[:blank:]]+", "")
    message.send(norikae(station))


# 終電を検索する


def norikae(eki1):
    query = {
        "eki1": eki1,
        "eki2": eki2
    }
    req = urllib.parse.urlencode(query)
    res = urllib.request.urlopen(url_norikae + req)
    source = res.read().decode("utf-8")
    source = source.split("<hr size=\"1\" color=\"black\" />")[2]
    return source
