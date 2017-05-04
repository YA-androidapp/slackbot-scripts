# -*- coding: utf-8 -*-
# Copyright (c) 2017 YA-androidapp(https://github.com/YA-androidapp) All
# rights reserved.

import urllib.parse
import urllib.request
from html.parser import HTMLParser

from slackbot.bot import respond_to
from slackbot.bot import listen_to

# 定数
url_n225 = "http://indexes.nikkei.co.jp/nkave"

# 処理


@respond_to("日経")
@listen_to("日経平均")
def listen_n225(message):
    info = check_n225()
    message.reply(info)
    if info.find(" ＋") > -1:
        message.react("smile")
    elif info.find(" -") > -1:
        message.react("cry")


# 日経平均を確認する
def check_n225():
    res = urllib.request.urlopen(url_n225)
    parser = N225Parser()
    parser.feed(res.read().decode("utf-8"))
    parser.close()
    return parser.get_info()

# 日経平均をパース


class N225Parser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.flag = 0
        self.info = ""

    def get_info(self):
        return self.info

    def handle_data(self, data):
        if self.flag == 1:
            self.info += data
            self.flag = 0
        elif self.flag == 2:
            self.info += " " + data
            self.flag = 0

    def handle_starttag(self, tag, attrs):
        if tag == "div":  # <div>タグを拾う
            attrs = dict(attrs)
            if "class" in attrs:
                # <div class="top-nk225-value">タグを拾う
                if attrs["class"] == "top-nk225-value":
                    self.flag = 1
                elif attrs["class"] == "top-nk225-differ":
                    self.flag = 2
