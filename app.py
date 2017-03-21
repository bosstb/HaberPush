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

#leancloud.init("96Q4GMOz0VpK4JwfeUjEHNWC-MdYXbMMI", "aCAfwt702pPeubx6tnngUWiu")


clickList = {}
clickListIsInit = False
app = Flask(__name__)
sockets = Sockets(app)
# 动态路由
app.register_blueprint(todos_view, url_prefix='/todos')


class AndroidId(leancloud.Object):
    pass


class AndroidIdRepeat(leancloud.Object):
    pass


class PostTest(leancloud.Object):
    pass


class CloudControl(leancloud.Object):
    pass


class ClickRecord(leancloud.Object):
    pass


class AffiliateSetting(leancloud.Object):
    pass


@app.route('/', methods=["GET", "POST"])
def index():
    #POST方法判断
    if request.method == "POST":
        #请求内容类型判断
        print request.get_data()
        if request.content_type == "text/plain;charset=UTF-8":
            args = json.loads(request.get_data())
        else:
            args = request.form
        sourceId = args.get('sourceId')
        title =  args.get('title')


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
    else:
        return "不支持Get"
def clickListInit():
    query = leancloud.Query(ClickRecord)
    query.greater_than('time', datetime.today()-timedelta(seconds=3600))
    query_list = query.find()
    for item in query_list:
        clickList[item.get('ipua')] = dict(item.get('clickInfo'))
    clickListIsInit = True


@app.route('/time')
def time():
    return str(datetime.now())


@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)


if __name__ == '__main__':
    app.run('0.0.0.0')

