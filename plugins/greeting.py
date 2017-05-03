# -*- coding: utf-8 -*-
# Copyright (c) 2017 YA-androidapp(https://github.com/YA-androidapp) All
# rights reserved.

from slackbot.bot import listen_to


@listen_to("おきた")
@listen_to("起きた")
@listen_to("おはよう")
def morning(message):
    message.reply("おはよう！")


@listen_to("いってくる")
@listen_to("行ってくる")
@listen_to("いってきます")
@listen_to("行ってきます")
def takecare(message):
    message.reply("いってらっしゃい！")


@listen_to("帰宅")
@listen_to("きたく")
@listen_to("ただいま")
def welcomehome(message):
    message.reply("おかえり！")


@listen_to("寝")
@listen_to("おやすみ")
def night(message):
    message.reply("おやすみ！")
