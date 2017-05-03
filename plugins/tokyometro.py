# -*- coding: utf-8 -*-
# Copyright (c) 2017 YA-androidapp(https://github.com/YA-androidapp) All
# rights reserved.

import urllib.parse
import urllib.request
from html.parser import HTMLParser

from slackbot.bot import respond_to
from slackbot.bot import listen_to

# 定数
url_tokyometro_names = [
    "銀座線",
    "丸ノ内線",
    "日比谷線",
    "東西線",
    "千代田線",
    "有楽町線",
    "半蔵門線",
    "南北線",
    "副都心線"
]

url_tokyometro_h = "http://www.tokyometro.jp/unkou/history/"
url_tokyometro_routes = [
    "ginza",
    "marunouchi",
    "hibiya",
    "touzai",
    "chiyoda",
    "yurakucho",
    "hanzoumon",
    "nanboku",
    "fukutoshin"
]
url_tokyometro_f = ".html"

# 処理


@respond_to("メトロ")
@respond_to("東京メトロ")
@respond_to("地下鉄")
@respond_to("運行")
@listen_to("メトロ")
@listen_to("東京メトロ")
@listen_to("地下鉄")
@listen_to("運行")
def listen_tokyometro(message):
    i = 0
    for route in url_tokyometro_routes:
        info = url_tokyometro_names[i] + ": " + check_tokyometro(route)
        message.reply(info)
        i += 1


@respond_to("銀座線")
@listen_to("銀座線")
def listen_tokyometro0(message):
    info = check_tokyometro(url_tokyometro_routes[0])
    message.reply(info)
    if info == "現在、平常どおり運転しています。":
        message.react("+1")


@respond_to("丸ノ内線")
@respond_to("丸の内線")
@listen_to("丸ノ内線")
@listen_to("丸の内線")
def listen_tokyometro1(message):
    info = check_tokyometro(url_tokyometro_routes[1])
    message.reply(info)
    if info == "現在、平常どおり運転しています。":
        message.react("+1")


@respond_to("日比谷線")
@listen_to("日比谷線")
def listen_tokyometro2(message):
    info = check_tokyometro(url_tokyometro_routes[2])
    message.reply(info)
    if info == "現在、平常どおり運転しています。":
        message.react("+1")


@respond_to("東西線")
@listen_to("東西線")
def listen_tokyometro3(message):
    info = check_tokyometro(url_tokyometro_routes[3])
    message.reply(info)
    if info == "現在、平常どおり運転しています。":
        message.react("+1")


@respond_to("千代田線")
@listen_to("千代田線")
def listen_tokyometro4(message):
    info = check_tokyometro(url_tokyometro_routes[4])
    message.reply(info)
    if info == "現在、平常どおり運転しています。":
        message.react("+1")


@respond_to("有楽町線")
@listen_to("有楽町線")
def listen_tokyometro5(message):
    info = check_tokyometro(url_tokyometro_routes[5])
    message.reply(info)
    if info == "現在、平常どおり運転しています。":
        message.react("+1")


@respond_to("半蔵門線")
@listen_to("半蔵門線")
def listen_tokyometro6(message):
    info = check_tokyometro(url_tokyometro_routes[6])
    message.reply(info)
    if info == "現在、平常どおり運転しています。":
        message.react("+1")


@respond_to("南北線")
@listen_to("南北線")
def listen_tokyometro7(message):
    info = check_tokyometro(url_tokyometro_routes[7])
    message.reply(info)
    if info == "現在、平常どおり運転しています。":
        message.react("+1")


@respond_to("副都心線")
@listen_to("副都心線")
def listen_tokyometro8(message):
    info = check_tokyometro(url_tokyometro_routes[8])
    message.reply(info)
    if info == "現在、平常どおり運転しています。":
        message.react("+1")


# 東京メトロの運行状況を確認する
def check_tokyometro(route):
    res = urllib.request.urlopen(url_tokyometro_h + route + url_tokyometro_f)
    parser = TokyometroParser()
    parser.feed(res.read().decode("utf-8"))
    parser.close()
    return parser.get_info()

# 東京メトロの運行情報をパース


class TokyometroParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.flag = False
        self.info = ""

    def get_info(self):
        return self.info

    def handle_data(self, data):
        if self.flag:
            self.info = data
            self.flag = False

    def handle_starttag(self, tag, attrs):
        if tag == "p":  # <p>タグを拾う
            attrs = dict(attrs)
            if "class" in attrs:
                if attrs["class"] == "v2_sectionMS":  # <p class="v2_sectionMS">タグを拾う
                    self.flag = True
