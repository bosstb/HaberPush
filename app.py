# coding: utf-8
#遗留问题：IP会变：54.193.59.55


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


class pushRecord(leancloud.Object):
    pass


@app.route('/', methods=["GET", "POST"])
def index():
    #POST方法判断
    # if request.method == "POST":
    #     #请求内容类型判断
    #     req = request
    #     print '111'
    #     if request.content_type == "application/json; charset=utf-8":
    #         args = json.loads(request.get_data())
    #     else:
    #         args = request.form
    #     #content_json = json.loads(args.get('json'))
    #     content_json = json.loads('[{"id":"5QyqDq1HmU_","title":"İçişleri Bakanı Soylu: Terör örgütünün şehir yapılanması tamamen çökertildi"},{"id":"5Qyr4qSnOLI","title":"Kılıçdaroğlu: Kutuplaşma kaygı verici"},{"id":"5Qyy2Xt1wrD","title":"Amazon CEO’su dünyayı kurtarma provası yaptı"},{"id":"5QywT2J1raV","title":"İFF’den SABAH ve atv’ye teşekkür"},{"id":"5QyrNeOXzlg","title":"Garnizon komutanına FETÖ gözaltısı"}]')
    #     for item in content_json:
    #         print item
    #         sourceId = args.get('sourceId')
    #         title = args.get('title')


        # if user_androidId != None:
        #     print user_androidId
        #     query = leancloud.Query(AndroidId)
        #     query.equal_to('ai', user_androidId)
        #     query_list = query.find()
        #     # 取国家
        #     r = requests.post(
        #         'http://api.db-ip.com/v2/c6f4413393e0ce3d120471ad41f7d7ad5bf77df0/' + str(ip))
        #     country = json.loads(r.text)
        #     if r.text.find('error') == -1:
        #         if country["countryCode"] != 'ZZ':
        #             countryName = country["countryName"]
        #         else:
        #             countryName = 'Unkown'
        #     else:
        #         countryName = 'Unkown'
        #     if len(query_list) == 0:
        #         #判断安卓Id是否存在
        #         androidId.set('ai', user_androidId)
        #         androidId.set('aa', aa)
        #         androidId.set('mo', mo)
        #         androidId.set('nt', nt)
        #         androidId.set('oc', oc)
        #         androidId.set('vn', vn)
        #         androidId.set('lang', lang)
        #         androidId.set('an', an)
        #         androidId.set('IP', ip)
        #         androidId.set('ua', ua)
        #         androidId.set('on', on)
        #         androidId.set('pkg', pkg)
        #         androidId.set('me', me)
        #         androidId.set('ms', ms)
        #         androidId.set('cn', countryName)
        #         androidId.set('clickInfo', clickInfo)
        #         androidId.save()
    return "OK"
    # else:
    #     return "不支持Get"
def PushTest():
    content_json = json.loads(
        '[{"id":"5QyqDq1HmU_","title":"İçişleri Bakanı Soylu: Terör örgütünün şehir yapılanması tamamen çökertildi"},{"id":"5Qyr4qSnOLI","title":"Kılıçdaroğlu: Kutuplaşma kaygı verici"},{"id":"5Qyy2Xt1wrD","title":"Amazon CEO’su dünyayı kurtarma provası yaptı"},{"id":"5QywT2J1raV","title":"İFF’den SABAH ve atv’ye teşekkür"},{"id":"5QyrNeOXzlg","title":"Garnizon komutanına FETÖ gözaltısı"}]')
    for item in content_json:
        print item
        sourceId = item.get('id')
        title = item.get('title')
        print sourceId+title


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
        #r = requests.get('192.168.10.101:8801/v1/custompush/news')
        content_json = json.loads(
            '[{"id":"5QyqDq1HmU_","title":"İçişleri Bakanı Soylu: Terör örgütünün şehir yapılanması tamamen çökertildi"},{"id":"5Qyr4qSnOLI","title":"Kılıçdaroğlu: Kutuplaşma kaygı verici"},{"id":"5Qyy2Xt1wrD","title":"Amazon CEO’su dünyayı kurtarma provası yaptı"},{"id":"5QywT2J1raV","title":"İFF’den SABAH ve atv’ye teşekkür"},{"id":"5QyrNeOXzlg","title":"Garnizon komutanına FETÖ gözaltısı"}]')
        pushInfo = ''
        for item in content_json:
            print item
            sourceId = item.get('id')
            title = item.get('title')
            pushInfo = pushInfo + '<\br>' + '<a href = "https://compaign.newsgrapeapp.com/news/' + sourceId + '">' + title + '</a>' + '&nbsp;&nbsp;&nbsp;' + \
            '<a href = "http://haberpush.leanapp.cn/' + sourceId + '?title=' + title + '">Push</a>'
            print sourceId + title

        replyStr = '<xml><ToUserName>' + FromUserName + '</ToUserName>' + '<FromUserName>' + ToUserName + '</FromUserName>' + '<CreateTime>' + \
        str(time.mktime(datetime.datetime.now().timetuple())).split('.')[0] + '</CreateTime>' + '<MsgType><![CDATA[text]]></MsgType>' + \
        '<Content><![CDATA[' + pushInfo + ']]></Content></xml>'
        if Content == 'Push':
            return replyStr
        else:
            return "不支持的参数！"

    #获取接入Token
def getAccessToken():
    r = requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + appId + 'secret=' + appSecret)
    return r.text


@app.route('/<sourceId>', methods=['POST', 'GET'])
def videoDetail(sourceId):
    title = request.args.__getattribute__('title')
    if request.method == 'GET':
        mkdir_str = '{"platform":"all","audience":"all","notification":{"alert":' + sourceId + ',' \
                    '"android":{},"ios":{"extras":{ \
                "newsid":' + title + '}}}}'
        mkdir_url = "https://api.jpush.cn/v3/push"
        user = base64.encodestring("789dd28284380ec8a5137432:35ba7cba0791d95ad4586120").replace('\n', '')
        headder = {"Content-Type": "application/json", "Content-Length": str(len(mkdir_str)), "Authorization": 'Basic ' + user}
        r = requests.post(mkdir_url, data=mkdir_str.encode('utf-8'), headers=headder)
    return r.text



@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)


if __name__ == '__main__':
    app.run('0.0.0.0')

