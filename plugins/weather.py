# -*- coding: utf-8 -*-
# Copyright (c) 2017 YA-androidapp(https://github.com/YA-androidapp) All
# rights reserved.

import urllib.parse
import urllib.request
import json
import datetime
from html.parser import HTMLParser

from slackbot.bot import respond_to
from slackbot.bot import listen_to
# from slackbot.bot import default_reply

# 定数
appkey_owm = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
url_owm = "http://api.openweathermap.org/data/2.5/forecast?"
url_tenkijp_dress = "http://www.tenki.jp/lite/indexes/dress/3/16/4410.html"

# 処理


@respond_to("weather")
def mention_weather(message):
    location = message.body["text"] \
        .replace(r"@[^\s]+", "") \
        .replace("weather", "") \
        .replace(" at ", "") \
        .replace(" in ", "") \
        .replace(r"[[:blank:]]+", "")
    message.reply(get_owm(location))


@listen_to("服装")
def listen_dress(message):
    message.reply(get_tenkijp_dress())


@listen_to("天気")
def listen_weather(message):
    message.send(get_owm("Tokyo"))


# 該当なし
# count_failure = 0
# @default_reply()
# def default_func(message):
#     global count_failure
#     text = message.body["text"]

#     count_failure += 1
# message.reply("%d 回失敗しました\n```" + text + "```" % count_failure)  # メンション

# OpenWeatherMapから天気情報を取得する

def get_owm(location):
    location = location + ", Japan"
    query = {
        "q": location,
        "mode": "json",
        "units": "metric",
        "cnt": "1",
        "appid": appkey_owm,
    }
    req = urllib.parse.urlencode(query)
    res = urllib.request.urlopen(url_owm + req)
    json_str = res.readline()
    decoded_str = json.loads(json_str.decode("utf-8"))
    weather = decoded_str["list"][0]["weather"][0]["icon"].replace("n", "d")
    city = decoded_str["city"]["name"]
    date = decoded_str["list"][0]["dt"]
    date_str = datetime.datetime.fromtimestamp(date).strftime("%d")
    temp_max = decoded_str["list"][0]["main"]["temp_max"]  # 最高気温
    temp_min = decoded_str["list"][0]["main"]["temp_min"]  # 最低気温
    hum = decoded_str["list"][0]["main"]["humidity"]  # 湿度
    if weather == "01d":
        w_str = "快晴"
    elif weather == "02d":
        w_str = "晴れ"
    elif weather == "03d" or weather == "04d":
        w_str = "曇り"
    elif weather == "09d":
        w_str = "小雨"
    elif weather == "10d":
        w_str = "雨"
    elif weather == "11d":
        w_str = "雷雨"
    elif weather == "13d":
        w_str = "雪"
    elif weather == "50d":
        w_str = "霧"
    else:
        w_str = "不明"
    return city + "の" + date_str + "日の天気は" + w_str + ", " + \
        str(temp_max) + "/" + str(temp_min) + "℃, " + \
        "湿度" + str(hum) + "%です"

# tenki.jpから服装指数予報のコメントを取得する


def get_tenkijp_dress():
    res = urllib.request.urlopen(url_tenkijp_dress)
    parser = TenkijpDressParser()
    parser.feed(res.read().decode("utf-8"))
    parser.close()
    return parser.get_telop()

# tenki.jpの服装指数予報をパース


class TenkijpDressParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.flag = False
        self.telop = ""

    def get_telop(self):
        return self.telop

    def handle_data(self, data):
        if self.flag:
            self.telop = data
            self.flag = False

    def handle_starttag(self, tag, attrs):
        if tag == "p":  # <p>タグを拾う
            attrs = dict(attrs)
            if "class" in attrs:
                # <td class="forecast_index_today_tomorrow_telop">タグを拾う
                if attrs["class"] == "forecast_index_today_tomorrow_telop":
                    self.flag = True
