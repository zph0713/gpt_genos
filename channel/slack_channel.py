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
