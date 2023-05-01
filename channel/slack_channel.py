import re
import json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from common.config import load_config
from models.openai_model import OpenAIModel





app = App(token=load_config()['channels']['slack']['slack_bot_token'])
handler = SocketModeHandler(app, load_config()['channels']['slack']['slack_app_token'])

@app.event("message")
def handle_message_events(body, say):
    user_id = body['event']['user']
    channel_id = body['event']['channel']

    conversations = app.client.conversations_history(
        token=load_config()['channels']['slack']['slack_bot_token'],
        channel=channel_id,
        limit=4096,
    )
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
        'conversation_context': conversation_list[::-1],
        'current_message': body['event']['text'],
    }
    reply_content = SlackChannel().handle_message(conversation_info)
    say(reply_content)



        
class SlackChannel():
    def startup(self):
        handler.start()
        print("Slack channel is running...")

    # def cache_conversation(self, conversation_id, conversation_context):
    #     pass

    def handle_message(self, message):
        # conversation_id = message['conversation_id']
        conversation_context = message['conversation_context']
        current_message = message['current_message']
        if current_message == conversation_context[-1]:
            plain_text = re.sub(r'<@\w+>', '', current_message)
            conversation_context[-1] = {
                'role': 'user',
                'content': plain_text
            }
        else:
            if current_message == '':
                return 'no input'
            else:
                conversation_context.append({
                    'role': 'user',
                    'content': current_message
                })
        print(conversation_context)
        return OpenAIModel().reply(conversation_context)
