# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 12:28:37 2020

@author: Tobias
"""

import facebook
app_token='2564243073845967|vAXGd57VXc0cDQGlnuwNZxX3BII'
def get_fb_auth():
    access_token = "EAAkcKl2Iys8BANYDSnHm2aeQS5r5hmhm7kGtCUK3kVcHwmgvAR5MqxPgVuryoRq661hpdZCfvBTZBe5e5tS0Wf6dQGE11JGbw9HwDAEuQ1NZA0klmuZCLZBcztdZBhqrD8xEJ43VIZCeXvEqBS57BnDGTDTUtg7IAl1DHq2D1PZB7yoQ7cbmSpraJkzlnaMRySZAcuTYqmyIXYh1eZC9Lcgbx1"
    graph = facebook.GraphAPI(access_token=app_token, version="2.12")
    app_id = "2564243073845967"
    canvas_url = "https://localhost/"
    perms = ["manage_pages","publish_pages"]
    fb_login_url = graph.get_auth_url(app_id, canvas_url, perms)
    print(fb_login_url)
def post_to_Facebook(message):
    access_token = "EAAkcKl2Iys8BANYDSnHm2aeQS5r5hmhm7kGtCUK3kVcHwmgvAR5MqxPgVuryoRq661hpdZCfvBTZBe5e5tS0Wf6dQGE11JGbw9HwDAEuQ1NZA0klmuZCLZBcztdZBhqrD8xEJ43VIZCeXvEqBS57BnDGTDTUtg7IAl1DHq2D1PZB7yoQ7cbmSpraJkzlnaMRySZAcuTYqmyIXYh1eZC9Lcgbx1"
    graph = facebook.GraphAPI(access_token=access_token, version="2.12")
    facebook_page_id = "103180454657684"
    graph.put_object(facebook_page_id, "feed", message=message)
get_fb_auth()
    

