# coding: utf-8
#遗留问题：IP会变：54.193.59.55

import os
from datetime import datetime
from datetime import timedelta
import json
from flask import Flask,redirect
from flask import render_template
from flask_sockets import Sockets
import random
from views.todos import todos_view
from flask import request
import leancloud
import requests
import xml.dom.minidom
import datetime
import time
import base64
#leancloud.init("96Q4GMOz0VpK4JwfeUjEHNWC-MdYXbMMI", "aCAfwt702pPeubx6tnngUWiu")


app = Flask(__name__)
sockets = Sockets(app)
# 动态路由
app.register_blueprint(todos_view, url_prefix='/todos')
#微信公众号定义
appSecret = 'ba8cfd77977f3f9a57eccaa1b00c7903'
appId = 'wxe9b54103e44bd336'
lastTitle = ''


class pushRecord(leancloud.Object):
    pass





@app.route('/', methods=["GET", "POST"])
def index():
    return "OK"


# def PushTest():
#     content_json = json.loads(
#         '[{"id":"5QyqDq1HmU_","title":"İçişleri Bakanı Soylu: Terör örgütünün şehir yapılanması tamamen çökertildi"},{"id":"5Qyr4qSnOLI","title":"Kılıçdaroğlu: Kutuplaşma kaygı verici"},{"id":"5Qyy2Xt1wrD","title":"Amazon CEO’su dünyayı kurtarma provası yaptı"},{"id":"5QywT2J1raV","title":"İFF’den SABAH ve atv’ye teşekkür"},{"id":"5QyrNeOXzlg","title":"Garnizon komutanına FETÖ gözaltısı"}]')
#     for item in content_json:
#         print item
#         sourceId = item.get('id')
#         title = item.get('title')
#         print sourceId+title


@app.route('/time')
def timea():
    return str(datetime.now())


@app.route('/wechatapi', methods=["GET", "POST"])
def wechat():
    #请求内容类型判断
    if request.method == 'GET':
        args = request.args
        signature = args.get('signature')
        timestamp = args.get('timestamp')
        nonce = args.get('nonce')
        echostr = args.get('echostr')
        if echostr != None:
            print echostr
            return echostr
        else:
            print 'None'
            return 'None'
    elif request.method =='POST':
        args = request.get_data()
        doc = xml.dom.minidom.parseString(args)
        doc = xml.dom.minidom.parseString(args)
        ToUserName = doc.getElementsByTagName("ToUserName")[0].firstChild.data
        FromUserName = doc.getElementsByTagName("FromUserName")[0].firstChild.data
        print FromUserName
        CreateTime = doc.getElementsByTagName("CreateTime")[0].firstChild.data
        MsgType = doc.getElementsByTagName("MsgType")[0].firstChild.data
        Content = doc.getElementsByTagName("Content")[0].firstChild.data
        MsgId = doc.getElementsByTagName("MsgId")[0].firstChild.data

        content_json = json.loads(getPushContent())
        pushInfo = ''
        for item in content_json:
            sourceId = item.get('id')
            title = item.get('title')
            content = item.get('content')
            publishedTime = str(item.get('publishedTime')).replace('+0000', '').replace('T', ' ')
            pushInfo = pushInfo + '===============================' + '<a href = "https://compaign.newsgrapeapp.com/news/' + \
                       sourceId + '">' + title + ' [' + str(publishedTime) + '] </a>' + '+++++++' + \
            '<a href = "http://haberpush.leanapp.cn/' + sourceId + '?title=' + title + '&content=' + content + '">Push</a>'
        replyStr = '<xml><ToUserName>' + FromUserName + '</ToUserName>' + '<FromUserName>' + ToUserName + '</FromUserName>' + '<CreateTime>' + \
        str(time.mktime(datetime.datetime.now().timetuple())).split('.')[0] + '</CreateTime>' + '<MsgType><![CDATA[text]]></MsgType>' + \
        '<Content><![CDATA[' + pushInfo + ']]></Content></xml>'
        if Content == 'Push':
            print replyStr.encode('utf-8')
            return replyStr.encode('utf-8')
        else:
            return "不支持的参数！"


def getPushToken():
        r = requests.get(
            'https://api.newsgrapeapp.com/auth/token?udid=123456&platform=WEB&pcid=123')
        return r.text


def getPushContent():
    # 取Token:
    BASE_DIR = os.path.dirname(__file__)  # 获取当前文件夹的父目录绝对路径
    print BASE_DIR
    file_path = os.path.join(BASE_DIR, 'static', 'token.txt')  # 获取C文件夹中的的Test_Data文件
    f = open(file_path, 'r')
    token = ''
    token = f.read()
    headers = {'Authorization': 'Bearer ' + token}
    f.close
    r = requests.get('https://api.newsgrapeapp.com/v1/custompush/news', headers=headers)
    while r.text.find('"error":"Unauthorized"') > 0:
        token = getPushToken()
        f = open(file_path, 'w')
        token = json.loads(token).get('accessToken')
        f.write(token)
        f.close()
        headers = {'Authorization': 'Bearer ' + token}
        r = requests.get('https://api.newsgrapeapp.com/v1/custompush/news', headers=headers)

    return r.text


    #获取接入Token
def getAccessToken():
    r = requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + appId + 'secret=' + appSecret)
    return r.text


@app.route('/<sourceId>', methods=['POST', 'GET'])
def push(sourceId):
    global lastTitle
    title = request.args.get('title')
    content = request.args.get('content')
    if request.method == 'GET' and lastTitle != title:
        mkdir_str = '{"platform":"all","audience":"all","notification":{"alert":{"title":"' + title + '","body":"' + content + '"},"android":{},"ios":{"extras":{ \
                "news_id":"' + sourceId + '"}}}}'
        mkdir_url = "https://api.jpush.cn/v3/push"
        user = base64.encodestring("789dd28284380ec8a5137432:35ba7cba0791d95ad4586120").replace('\n', '')
        headder = {"Content-Type": "application/json", "Content-Length": str(len(mkdir_str)), "Authorization": 'Basic ' + user}
        r = requests.post(mkdir_url, data=mkdir_str.encode('utf-8'), headers=headder)
    lastTitle = title
    return r.text



@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)


if __name__ == '__main__':
    app.run('0.0.0.0')

