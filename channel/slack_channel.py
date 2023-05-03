import re
import json
import sys
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from common.base import load_config,log
from core.selector import ModelSelector




app = App(token=load_config()['channels']['slack']['slack_bot_token'])
handler = SocketModeHandler(app, load_config()['channels']['slack']['slack_app_token'])

@app.event("message")
def handle_message_events(body, say):
    user_id = body['event']['user']
    channel_id = body['event']['channel']
    log.info(f"User {user_id} in Channel {channel_id} says: {body['event']['text']}")
    try:
        conversations = app.client.conversations_history(
            token=load_config()['channels']['slack']['slack_bot_token'],
            channel=channel_id,
            limit=4096,
        )
    except Exception as e:
        log.error(e)
        log.warning("I can't connect to the slack, please check your network connection")
        return "我连接不到slack，请稍后重试"
    conversation_context = conversations['messages']
    conversation_list = []
    for conversation in conversation_context:
        if conversation['user'] == user_id:
            conversation['role'] = 'user'
        else:
            conversation['role'] = 'assistant'
        conversation_format = {
            'role': conversation['role'],
            'content': conversation['text']
        }
        conversation_list.append(conversation_format)
    conversation_info = {
        'conversation_id': channel_id,
        'conversation_context': conversation_list,
        'current_message': body['event']['text'],
    }
    reply_content = SlackChannel().handle_message(conversation_info)
    log.info(f"Bot replies: {reply_content}")
    say(reply_content)



        
class SlackChannel():
    def startup(self):
        handler.start()
        log.info("Slack channel is running...")

    def handle_message(self, message):
        conversation_context = message['conversation_context']
        current_message = message['current_message']
        if current_message == conversation_context[0]['content']:
            log.info('last converation is the same as current message...')
            log.info('previous conversation: %s'%conversation_context[1]['content'])
            plain_text = re.sub(r'<@\w+>', '', current_message)
            conversation_context[-1] = {
                'role': 'user',
                'content': plain_text
            }
        else:
            if current_message == '':
                log.info('no input...')
                return 'no input'
            else:
                last_3_conv = conversation_context[-3:]
                log.info('last 3 conversation: %s'%last_3_conv)
                conversation_context.append({
                    'role': 'user',
                    'content': current_message
                })
        # 将list的元素index反序
        conversation_context.reverse()
        message_length = sum([len(i['content']) for i in conversation_context])
        # 如果message_length大于4096，就删除第一个元素，直到message_length小于4096
        while message_length > 4096:
            conversation_context.pop(0)
            message_length = sum([len(i['content']) for i in conversation_context])
        log.info('current message length: %s'%message_length)
        model = ModelSelector(load_config()['type_choices']['model']).create_model()
        return model.reply(conversation_context)
