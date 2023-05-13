from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from common.base import load_config,log
from core.selector import ModelSelector
from core.conversation_cache import ConversationCache




app = App(token=load_config()['channels']['slack']['slack_bot_token'])
handler = SocketModeHandler(app, load_config()['channels']['slack']['slack_app_token'])

@app.event("message")
def handle_message_events(body, say):
    user_id = body['event']['user']
    channel_id = body['event']['channel']
    if body['event']['text'] == '#clear':
        ConversationCache('slack',channel_id).clear_msg()
        log.info(f"User {user_id} in Channel {channel_id} says: {body['event']['text']}")
        say('对话已清空')
    elif body['event']['text'] == '#cache':
        conversations = ConversationCache('slack',channel_id).get_msg()
        log.info(f"User {user_id} in Channel {channel_id} says: {body['event']['text']}")
        cache_info = {
            'conversations_count': len(conversations),
            'conversations_length': sum([len(str(i)) for i in conversations]),
            'last_conversation': conversations[-1],
            'previous_conversation': conversations[-2],
            'first_conversation': conversations[0],
            'second_conversation': conversations[1]
        }
        # 将缓存信息以表格形式返回
        say(f"```{cache_info}```")
    elif body['event']['text'] == '#help':
        log.info(f"User {user_id} in Channel {channel_id} says: {body['event']['text']}")
        say('输入#clear清空对话，输入#cache查看cache对话，输入#help查看帮助')
    else:
        ConversationCache('slack',channel_id).save_msg('user',body['event']['text'])
        log.info(f"User {user_id} in Channel {channel_id} says: {body['event']['text']}")
        conversations = ConversationCache('slack',channel_id).get_msg()
        reply_content = SlackChannel().handle_message(conversations)
        ConversationCache('slack',channel_id).save_msg('assistant',reply_content)
        log.info(f"Bot replies: {reply_content}")
        say(reply_content)



class SlackChannel():
    def startup(self):
        handler.start()
        log.info("Slack channel is running...")

    def handle_message(self, conversation_context):
        model = ModelSelector(load_config()['type_choices']['model']).create_model()
        return model.reply(conversation_context)
