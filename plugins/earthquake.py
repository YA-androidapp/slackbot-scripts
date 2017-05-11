# -*- coding: utf-8 -*-
# Copyright (c) 2017 YA-androidapp(https://github.com/YA-androidapp) All
# rights reserved.

import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

from slackbot.bot import respond_to
from slackbot.bot import listen_to

# 定数
url_quake = "http://www.jma.go.jp/jp/quake/quake_singen_index.html"

# 処理


@respond_to("地震")
@respond_to("ゆれ")
@respond_to("揺れ")
@listen_to("地震")
@listen_to("ゆれ")
@listen_to("揺れ")
def check_yure(message):
    info = check_earthquake()
    message.reply(info)


# 地震情報を確認する
def check_earthquake():
    res = urllib.request.urlopen(url_quake)
    htmlstr = res.read().decode("utf-8")
    return parse_html(htmlstr)

# 地震情報をパース


def parse_html(htmlstr):
    soup = BeautifulSoup(htmlstr)
    result = ""
    trs = soup.select("div.infotable tr")
    i = 0
    for tr_item in trs:
        if i > 0:  # ヘッダはスキップ
            tds = tr_item.find_all("td")
            j = 0
            for td_item in tds:
                if j > 0:  # 情報発表日時はスキップ
                    print(td_item)
                    result = result + td_item.text
                j += 1
            return result
        i += 1
