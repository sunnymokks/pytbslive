from flask import Flask, Response, redirect, url_for
from datetime import date, timedelta
from pyquery import PyQuery as pq
import requests
import urllib.parse
import dominate
from dominate.tags import *
from dominate.util import raw

app = Flask(__name__)

@app.route("/")
def root():
    return redirect(url_for("tbslive"), code=302)

@app.route("/tbslive")
def tbslive():
    doc = dominate.document(title="TBS")
    with doc.head:
        style("""
        .content {
            max-width: auto;
            margin: 20px;
            font-size: 24px;
        }
        """)
    with doc:
        with div(cls='content'):
            h1(a("西雅圖雷藏寺", href="http://www.tbsseattle.org"))
            link_list = _get_tbsseattle_live_list()
            for link in link_list:
                raw(link)
            br()
            hr()

            h1(a("台灣雷藏寺", href="https://tbsec.org/"))
            link_content = _get_tbstw_live_list()
            raw(link_content)
    
    return doc.render()


def _get_tbsseattle_live_list():
    resp = requests.get("http://www.tbsseattle.org/")
    dom = pq(resp.text)

    link_list = []
    menu_list = dom.find("li.menu-item")
    for m in menu_list:
        text = pq(m).text()
        if "網路直播" in text:
            live_list = pq(m).find("ul li")
            for live in live_list:
                link_list.append(pq(live).outer_html())
    return link_list

def _get_tbstw_live_list():
    ret = []
    resp = requests.get("https://tbsec.org/%E6%B3%95%E6%9C%83%E7%B7%9A%E4%B8%8A%E7%9B%B4%E6%92%AD")
    dom = pq(resp.text)

    live_content = dom.find("div.LiveContent:first")
    return pq(live_content).outer_html()
