# coding: utf-8

import time
import hashlib
import log
import db

from lxml import etree
from flask import request
from flask import Flask, make_response



"""
ToUserName: gh_27567063dafa
FromUserName: oy_yJwFbrb6apeafgMCr6MN09Y0U
<xml><ToUserName><![CDATA[oy_yJwFbrb6apeafgMCr6MN09Y0U]]></ToUserName>
<FromUserName><![CDATA[gh_27567063dafa]]></FromUserName>
<CreateTime>1666525888</CreateTime><MsgType>
<![CDATA[text]]></MsgType><Content><![CDATA[11111]]></Content>
</xml>
"""


app = Flask(__name__)


class Message(object):
    def __init__(self, req):
        self.request = req
        self.token = "Password"
        self.AppID = "wx55c55b0a86c5fd17"
        self.AppSecret = "qNs8mfj6pjj6k42z3PBzPs5uWTFQzRNNQdnJBQ8sLt2"


class Get(Message):
    def __init__(self, req):
        super(Get, self).__init__(req)
        self.signature = req.args.get('signature')  # 这里分别获取传入的四个参数
        self.timestamp = req.args.get('timestamp')
        self.nonce = req.args.get('nonce')
        self.echostr = req.args.get('echostr')
        self.return_code = 'Invalid'

    def verify(self):
        data = sorted([self.token, self.timestamp, self.nonce])  # 字典排序
        string = ''.join(data).encode('utf-8')  # 拼接成字符串
        hashcode = hashlib.sha1(string).hexdigest()  # sha1加密
        if self.signature == hashcode:
            self.return_code = self.echostr


class Post(Message):
    def __init__(self, req):
        super(Post, self).__init__(req)
        self.xml = etree.fromstring(req.stream.read())
        self.MsgType = self.xml.find("MsgType").text
        self.ToUserName = self.xml.find("ToUserName").text
        self.FromUserName = self.xml.find("FromUserName").text
        self.CreateTime = self.xml.find("CreateTime").text
        self.MsgId = self.xml.find("MsgId").text
        
        hash_table = {
            'text': ['Content'],
            'image': ['PicUrl', 'MediaId'],
            'voice': ['MediaId', 'Format'],
            'video': ['MediaId', 'ThumbMediaId'],
            'shortvideo': ['MediaId', 'ThumbMediaId'],
            'location': ['Location_X', 'Location_Y', 'Scale', 'Label'],
            'link': ['Title', 'Description', 'Url'],
        }
        attributes = hash_table[self.MsgType]
        self.Content = self.xml.find("Content").text if 'Content' in attributes else '抱歉，暂未支持此消息。'
        self.PicUrl = self.xml.find("PicUrl").text if 'PicUrl' in attributes else '抱歉，暂未支持此消息。'
        self.MediaId = self.xml.find("MediaId").text if 'MediaId' in attributes else '抱歉，暂未支持此消息。'
        self.Format = self.xml.find("Format").text if 'Format' in attributes else '抱歉，暂未支持此消息。'
        self.ThumbMediaId = self.xml.find("ThumbMediaId").text if 'ThumbMediaId' in attributes else '抱歉，暂未支持此消息。'
        self.Location_X = self.xml.find("Location_X").text if 'Location_X' in attributes else '抱歉，暂未支持此消息。'
        self.Location_Y = self.xml.find("Location_Y").text if 'Location_Y' in attributes else '抱歉，暂未支持此消息。'
        self.Scale = self.xml.find("Scale").text if 'Scale' in attributes else '抱歉，暂未支持此消息。'
        self.Label = self.xml.find("Label").text if 'Label' in attributes else '抱歉，暂未支持此消息。'
        self.Title = self.xml.find("Title").text if 'Title' in attributes else '抱歉，暂未支持此消息。'
        self.Description = self.xml.find("Description").text if 'Description' in attributes else '抱歉，暂未支持此消息。'
        self.Url = self.xml.find("Url").text if 'Url' in attributes else '抱歉，暂未支持此消息。'
        self.Recognition = self.xml.find("Recognition").text if 'Recognition' in attributes else '抱歉，暂未支持此消息。'
        
        log.RUNNLOG("Receive type: {0}, user: {1}".format(self.MsgType, self.ToUserName))

class Reply(Post):
    def __init__(self, req):
        super(Reply, self).__init__(req)
        self.xml = f'<xml><ToUserName><![CDATA[{self.FromUserName}]]></ToUserName>' \
            f'<FromUserName><![CDATA[{self.ToUserName}]]></FromUserName>' \
            f'<CreateTime>{str(int(time.time()))}</CreateTime>'

    def text(self, Content):
        self.xml += f'<MsgType><![CDATA[text]]></MsgType>' \
            f'<Content><![CDATA[{Content}]]></Content></xml>'

    def image(self, MediaId):
        pass

    def voice(self, MediaId):
        pass

    def video(self, MediaId, Title, Description):
        pass

    def music(self, ThumbMediaId, Title='', Description='', MusicURL='', HQMusicUrl=''):
        pass

    def reply(self):
        response = make_response(self.xml)
        response.content_type = 'application/xml'
        return response



def lst2msg(lst):
    res = ""
    for name, date, is_zh:
        is_zh_msg = "旧历" if is_zh else "新历"
        res += "%s, %s, %s\n" % (name, date, is_zh)
    return res


@app.route('/wx', methods=['GET', 'POST'])
def wechat():
    """
    增加-许-10月10日-旧历
    删除-许
    查询-许
    """
    if request.method == "GET":
        message = Get(request)
        message.verify()
        return message.return_code
    elif request.method == "POST":
        message = Reply(request)
        user_id = message.ToUserName
        lst = message.split("-")
        if lst[0] == "增加":
            name = lst[1]
            date = lst[2]
            is_zh = bool(lst[3])
            if not name or not date:
                res_msg = "输入错误"
            lst = db.manage.set(user_id, name, date, is_zh)
            res_msg = "增加成功!\n" + reslst2msg(lst)
        elif lst[0] == "删除":
            res_msg = "删除"
        elif lst[0] == "查询":
            pass
        else:
            res_msg = "请重新输入"
         
        
        
        message.text(message.Content)
        return message.reply()


if __name__ == '__main__':
    app.run()
