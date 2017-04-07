# coding: utf-8
#遗留问题：IP会变：54.193.59.55

import os
from datetime import datetime
from datetime import timedelta
import json
import youtube_dl
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
leancloud.init("fVBfU2NNnuRwhFLlrzIMy0ni-gzGzoHsz", "DXazg5nL3TfvtP3p3ad1zNVe")


app = Flask(__name__)
sockets = Sockets(app)
# 动态路由
app.register_blueprint(todos_view, url_prefix='/todos')
#微信公众号定义
appSecret = 'ba8cfd77977f3f9a57eccaa1b00c7903'
appId = 'wxe9b54103e44bd336'
lastTitle = ''


class NewsRecord(leancloud.Object):
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
        #print FromUserName
        CreateTime = doc.getElementsByTagName("CreateTime")[0].firstChild.data
        MsgType = doc.getElementsByTagName("MsgType")[0].firstChild.data
        msg = doc.getElementsByTagName("Content")[0].firstChild.data
        MsgId = doc.getElementsByTagName("MsgId")[0].firstChild.data
        content_json = json.loads(getPushContent(msg))
        pushInfo = ''
        count = 0
        for item in content_json:
            count += 1
            sourceId = item.get('id')
            title = item.get('title').replace('"', '').replace('\n', '')
            content = item.get('content').replace('"', '').replace('\n', '')
            newsRecord = NewsRecord()
            newsRecord.set('Id', sourceId)
            newsRecord.set('title', title)
            newsRecord.set('content', content)
            newsRecord.save()
            if msg == 'Push':
                publishedTime = str(item.get('publishedTime')).replace('+0000', '').replace('T', ' ')
            else:
                publishedTime = item.get('publishedTime')

            if msg.find('topic') >= 0:
                pushInfo = pushInfo + '|||' + 'TITLE:' + title + '|||' + content + 'CONTENT:'
            else:
                pushInfo = pushInfo + '|||' + '<a href="https://compaign.newsgrapeapp.com/news/' + \
                           sourceId + '">' + title + '(' + publishedTime + ')</a>' + '|||' + \
                '<a href="http://haberpush.leanapp.cn/wechatapi/' + sourceId + '">Push</a>'
                if msg != 'Push' and count > 5:
                    break

        replyStr = '<xml><ToUserName>' + FromUserName + '</ToUserName>' + '<FromUserName>' + ToUserName + '</FromUserName>' + '<CreateTime>' + \
        str(time.mktime(datetime.datetime.now().timetuple())).split('.')[0] + '</CreateTime>' + '<MsgType><![CDATA[text]]></MsgType>' + \
        '<Content><![CDATA[' + pushInfo + ']]></Content></xml>'
        print replyStr.encode('utf-8')
        return replyStr.encode('utf-8')


def getPushToken():
        r = requests.get(
            'https://api.newsgrapeapp.com/auth/token?udid=123456&platform=WEB&pcid=123')
        return r.text


def getPushContent(msg):
    # 取Token:
    BASE_DIR = os.path.dirname(__file__)  # 获取当前文件夹的父目录绝对路径
    #print BASE_DIR
    file_path = os.path.join(BASE_DIR, 'static', 'token.txt')  # 获取C文件夹中的的Test_Data文件
    f = open(file_path, 'r')
    token = ''
    token = f.read()
    headers = {'Authorization': 'Bearer ' + token}
    f.close
    if msg == 'Push':
        r = requests.get('https://api.newsgrapeapp.com/v1/custompush/news', headers=headers)
    elif msg.find('topic,') >= 0:
        r = requests.post('https://api.newsgrapeapp.com/v1/topic/news?topicId=' + str(msg).split(',')[1], headers=headers)
    elif msg.find('user,') >= 0:
        r = requests.get('https://api.newsgrapeapp.com/v1/custompush/usergroupnews?id=' + str(msg).split(',')[1] + '&score=' + str(msg).split(',')[2],
                          headers=headers)
        print 'https://api.newsgrapeapp.com/v1/custompush/usergroupnews?id=' + str(msg).split(',')[1] + 'score=' + str(msg).split(',')[2]
    else:
        r = requests.get('https://api.newsgrapeapp.com/v1/custompush/search?title=' + msg, headers=headers)
    while r.text.find('"error":"Unauthorized"') >= 0:
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


@app.route('/wechatapi/<sourceId>', methods=['POST', 'GET'])
def push(sourceId):
    query = leancloud.Query(NewsRecord)
    query.equal_to('Id', sourceId)
    query_list = query.find()
    title = query_list[0].get('title')
    content = query_list[0].get('content')
    global lastTitle
    if request.method == 'GET' and lastTitle != title:
        mkdir_str = '{"platform":"all","audience":"all","notification":{"alert":{"title":"' + title + '","body":"' + title + '"},"android":{},"ios":{"extras":{ \
                "news_id":"' + sourceId + '"}}}}'
        mkdir_url = "https://api.jpush.cn/v3/push"
        user = base64.encodestring("789dd28284380ec8a5137432:35ba7cba0791d95ad4586120").replace('\n', '')
        headder = {"Content-Type": "application/json", "Content-Length": str(len(mkdir_str)), "Authorization": 'Basic ' + user}
        r = requests.post(mkdir_url, data=mkdir_str.encode('utf-8'), headers=headder)
    lastTitle = title
    return r.text


@app.route('/getPlayURL')
def getPlayURL():
    args = request.args
    url = args.get("url")
    # format_url = args.get("format")
    if url == None:
        return "url missing"
    # if format_url == None:
    ydl_opts_getInfo = {'listformats': True, "simulate": True}
    # else:
    #     ydl_opts_getInfo = {'forceurl': True, 'format': format_url, "simulate": True}
    with youtube_dl.YoutubeDL(ydl_opts_getInfo) as ydl:
        return_msg = []
        message = ydl.download([str(url)])
        # if format_url == None:
        formats = message.get('formats', [message])
        for formatItem in formats:
            if formatItem.get('ext') in ('webm', 'mp4', 'mp3', '3gp', 'm4a', 'ogg'):
                fileSize = formatItem.get('filesize')
                if fileSize == None:
                    fileSize = ""
                duration = message.get('duration')
                if duration == None:
                    duration = ""
                thumbnail = message.get('thumbnail')
                if thumbnail == None:
                    thumbnail = ""
                dict = {'id': message.get('id'), 'duration': duration, 'format': formatItem.get('format'),
                        'title': message.get('title'),
                        'ext': formatItem.get('ext'), 'filesize': fileSize, 'thumbnail': thumbnail,
                        'url': formatItem.get('url')}
                return_msg.append(dict)
        return json.dumps(return_msg)








@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)


if __name__ == '__main__':
    app.run('0.0.0.0')

