# -*- coding: utf-8 -*-
# Copyright (c) 2017 YA-androidapp(https://github.com/YA-androidapp) All
# rights reserved.

import urllib.parse
import urllib.request
import json

from slackbot.bot import respond_to
from slackbot.bot import listen_to

# 定数
url_foreignexchange = "https://www.gaitameonline.com/rateaj/getrate"

# 処理


@respond_to("外為")
@listen_to("外為")
def listen_foreignexchange(message):
    info = check_foreignexchange("")
    message.reply(info)


@respond_to("ドル円")
@listen_to("ドル円")
def listen_foreignexchange_usd(message):
    info = check_foreignexchange("USD")
    message.reply(info)


# 日経平均を確認する
def check_foreignexchange(code):
    res = urllib.request.urlopen(url_foreignexchange)
    json_str = res.readline()
    decoded_str = json.loads(json_str.decode("utf-8"))
    quotes = decoded_str["quotes"]
    result = ""
    for item in quotes:
        if code == "" or item["currencyPairCode"].find(code) > -1:
            if item["currencyPairCode"].find("JPY") > -1:
                if code == "":
                    item_str = item["currencyPairCode"].replace("JPY", "") + \
                        ": " + item["bid"] + "/" + item["ask"]
                else:
                    item_str = item["bid"] + "/" + item["ask"]
                result += item_str + "\n"
            else:
                item_str = ""
        else:
            item_str = ""
    return result
