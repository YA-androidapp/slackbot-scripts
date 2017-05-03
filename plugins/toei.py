# -*- coding: utf-8 -*-
# Copyright (c) 2017 YA-androidapp(https://github.com/YA-androidapp) All
# rights reserved.

import urllib.parse
import urllib.request
from html.parser import HTMLParser

from slackbot.bot import respond_to
from slackbot.bot import listen_to

# 定数
url_toei_names = [
    "浅草線",
    "三田線",
    "新宿線",
    "大江戸線"
]

url_toei_h = "https://www.kotsu.metro.tokyo.jp/subway/schedule/"
url_toei_routes = [
    "asakusa",
    "mita",
    "shinjuku",
    "oedo"
]
url_toei_f = "_log.html"

# 処理


@respond_to("都営")
@respond_to("都営地下鉄")
@listen_to("都営")
@listen_to("都営地下鉄")
def listen_toei(message):
    i = 0
    for route in url_toei_routes:
        info = url_toei_names[i] + ": " + check_toei(route)
        message.reply(info)
        i += 1


@respond_to("浅草線")
@listen_to("浅草線")
def listen_toei0(message):
    info = check_toei(url_toei_routes[0])
    message.reply(info)
    if info == "現在、１５分以上の遅延はありません。":
        message.react("+1")


@respond_to("三田線")
@listen_to("三田線")
def listen_toei1(message):
    info = check_toei(url_toei_routes[1])
    message.reply(info)
    if info == "現在、１５分以上の遅延はありません。":
        message.react("+1")


@respond_to("新宿線")
@listen_to("新宿線")
def listen_toei2(message):
    info = check_toei(url_toei_routes[2])
    message.reply(info)
    if info == "現在、１５分以上の遅延はありません。":
        message.react("+1")


@respond_to("大江戸線")
@listen_to("大江戸線")
def listen_toei3(message):
    info = check_toei(url_toei_routes[3])
    message.reply(info)
    if info == "現在、１５分以上の遅延はありません。":
        message.react("+1")


# 都営地下鉄の運行状況を確認する
def check_toei(route):
    res = urllib.request.urlopen(url_toei_h + route + url_toei_f)
    parser = ToeiParser()
    parser.feed(res.read().decode("utf-8"))
    parser.close()
    return parser.get_info().replace(r"</?p>", "").replace("\n", "").replace(" ", "")

# 都営地下鉄の運行情報をパース


class ToeiParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.flag = False
        self.info = ""

    def get_info(self):
        return self.info

    def handle_data(self, data):
        if self.flag:
            self.info = self.info + data

    def handle_starttag(self, tag, attrs):
        if tag == "div":  # <div>タグを拾う
            attrs = dict(attrs)
            if "class" in attrs:
                # <div class="under-travelInfo__body">タグを拾う
                if attrs["class"] == "under-travelInfo__body":
                    self.flag = True

    def handle_endtag(self, tag):  # <div>タグの中の<p>タグにclass/idが付与されていないので若干回り道
        if self.flag:
            if tag == "div":  # 終了タグ
                self.flag = False
