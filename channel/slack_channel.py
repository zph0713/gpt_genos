from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from common.base import load_config,log
from core.selector import ModelSelector
from core.conversation_cache import ConversationCache
from channel.slack_blockkit import *




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
    elif body['event']['text'] == '#cache info':
        conversations = ConversationCache('slack',channel_id).get_msg()
        log.info(f"User {user_id} in Channel {channel_id} says: {body['event']['text']}")
        cache_info = {
            'conversations_count': len(conversations),
            'conversations_length': sum([len(str(i)) for i in conversations]),
            'user_conversations_count': len([i for i in conversations if i['role'] == 'user']),
            'assistant_conversations_count': len([i for i in conversations if i['role'] == 'assistant']),
            'system_conversations_count': len([i for i in conversations if i['role'] == 'system'])
        }
        say(cache_status(cache_info))

    elif body['event']['text'] == '#help':
        log.info(f"User {user_id} in Channel {channel_id} says: {body['event']['text']}")
        say('输入#clear清空对话，输入#cache查看cache对话，输入#help查看帮助')
    else:
        #如果是私聊，则直接回复
        if body['event']['channel_type'] == 'im':
            ConversationCache('slack',channel_id).save_msg('user',body['event']['text'])
            log.info(f"User {user_id} in Channel {channel_id} says: {body['event']['text']}")
            conversations = ConversationCache('slack',channel_id).get_msg()
            reply_content = SlackChannel().handle_message(conversations)
            ConversationCache('slack',channel_id).save_msg('assistant',reply_content)
            log.info(f"Bot replies: {reply_content}")
            say(reply_content)
        elif body['event']['channel_type'] == 'group':
            return


@app.event("app_mention")
def handle_mention(body, say):
    user_id = body['event']['user']
    channel_id = body['event']['channel']
    for authorization in body['authorizations']:
        if authorization['team_id'] == body['team_id'] and authorization['is_bot'] == True and authorization['user_id'] == body['event']['text'].split(' ')[0].replace('<@','').replace('>',''):
            bot_id = authorization['user_id']
            break
        else:
            return
    if body['event']['text'].split(' ')[0] == f'<@{bot_id}>':
        remove_at_text = body['event']['text'].replace(f'<@{bot_id}>','').replace(' ','')
        modify_text = body['event']['text'].replace(f'<@{bot_id}>','')
        if remove_at_text == '':
            say('Hi,什么事？',thread_ts=body['event']['ts'])
            return
        else:
            ConversationCache('slack',channel_id).save_msg('user',modify_text)
            log.info(f"User {user_id} in Channel {channel_id} says: {body['event']['text']}")
            conversations = ConversationCache('slack',channel_id).get_msg()
            reply_content = SlackChannel().handle_message(conversations)
            ConversationCache('slack',channel_id).save_msg('assistant',reply_content)
            log.info(f"Bot replies: {reply_content}")
            say(reply_content)
    else:
        return


    

    

    # #如果@机器人的时候，后面没有跟任何内容，则回复帮助信息

    # ConversationCache('slack',channel_id).save_msg('user',body['event']['text'])
    # log.info(f"User {user_id} in Channel {channel_id} says: {body['event']['text']}")
    # conversations = ConversationCache('slack',channel_id).get_msg()
    # reply_content = SlackChannel().handle_message(conversations)
    # ConversationCache('slack',channel_id).save_msg('assistant',reply_content)
    # log.info(f"Bot replies: {reply_content}")

    # say(text=reply_content,thread_ts=body['event']['ts'])
        


class SlackChannel():
    def startup(self):
        handler.start()
        log.info("Slack channel is running...")

    def shutdown(self):
        handler.close()
        log.info("Slack channel is closed...")

    def handle_message(self, conversation_context):
        model = ModelSelector(load_config()['type_choices']['model']).create_model()
        return model.reply(conversation_context)
