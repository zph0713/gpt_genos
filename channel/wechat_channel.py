import itchat
from itchat.content import *


@itchat.msg_register(TEXT)
def handler_single_msg(msg):
    WechatChannel().handle(msg)
    return None

@itchat.msg_register(TEXT, isGroupChat=True)
def handler_group_msg(msg):
    WechatChannel().handle_group(msg)
    return None



class WechatChannel():
    def __init__(self):
        pass

    def startup(self):
        itchat.auto_login(enableCmdQR=2, hotReload=True, qrCallback=self.login)
        itchat.run()

    def login(self, uuid=None, status='0', qrcode=None):
        print('uuid:', uuid)
        print('status:', status)
        print('qrcode_link:', 'https://login.weixin.qq.com/l/'+uuid)

    def handle(self, msg):
        print(msg)
        from_user_id = msg['FromUserName']
        to_user_id = msg['ToUserName']
        other_user_id = msg['User']['UserName']
        create_time = msg['CreateTime']
        content = msg['Text']

        hot_reload = True