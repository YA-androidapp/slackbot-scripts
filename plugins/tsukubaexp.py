# -*- coding: utf-8 -*-
# Copyright (c) 2017 YA-androidapp(https://github.com/YA-androidapp) All
# rights reserved.

import urllib.parse
import urllib.request
from html.parser import HTMLParser

from slackbot.bot import respond_to
from slackbot.bot import listen_to

# 定数
url_tx = "http://www.mir.co.jp/"

# 処理


@respond_to("tx")
@respond_to("TX")
@respond_to("つくばエクスプレス")
@listen_to("tx")
@listen_to("TX")
@listen_to("つくばエクスプレス")
def listen_tx(message):
    info = check_tx()
    message.reply(info)
    if info == "現在、平常通り運転しています。":
        message.react("+1")

# TXの運行状況を確認する


def check_tx():
    res = urllib.request.urlopen(url_tx)
    parser = TxParser()
    parser.feed(res.read().decode("utf-8"))
    parser.close()
    return parser.get_info().replace(r"</?p>", "").replace("\n", "")

# TXの運行情報をパース


class TxParser(HTMLParser):

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
        if tag == "td":  # <td>タグを拾う
            attrs = dict(attrs)
            if "class" in attrs:
                if attrs["class"] == "info-text":  # <td class="info-text">タグを拾う
                    self.flag = True

    def handle_endtag(self, tag):  # <td>タグの中の<p>タグにclass/idが付与されていないので若干回り道
        if self.flag:
            if tag == "td":  # 終了タグ
                self.flag = False
