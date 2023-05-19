from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from common.base import load_config,log
from core.selector import ModelSelector
from core.conversation_cache import ConversationCache
from core.chat_commands import chat_commands
from channel.slack_blockkit import *



app = App(token=load_config()['channels']['slack']['slack_bot_token'])
handler = SocketModeHandler(app, load_config()['channels']['slack']['slack_app_token'])

@app.event("message")
def handle_message_events(body, say):
    user_id = body['event']['user']
    channel_id = body['event']['channel']
    current_text = body['event']['text']
    channel_type = body['event']['channel_type'] 
    ts = body['event']['ts']

    command_check = chat_commands(channel_type,channel_id,ts,user_id,current_text).handle()
    if command_check != current_text:
        say(command_check)
        log.info(f"User {user_id} executes command in Channel {channel_id} at {ts}: {current_text}")
        return
    else:
        if channel_type == 'im':
            ConversationCache('slack',ts).save_msg('user',current_text)
            log.info(f"User {user_id} in Channel {channel_id} at {ts} says: {current_text}")
            conversations = ConversationCache('slack',ts).get_msg()
            reply_content = SlackChannel().handle_message(conversations)
            ConversationCache('slack',ts).save_msg('assistant',reply_content)
            log.info(f"Bot replies in Channel {channel_id} at {ts}: {reply_content}")
            say(reply_content)

        elif channel_type == 'group':
            bot_id = None
            if 'authorizations' in body:
                for authorization in body['authorizations']:
                    if authorization['is_bot'] == True:
                        bot_id = authorization['user_id']
                        break
                    else:
                        continue
            if bot_id:
                if 'thread_ts' in body['event']:
                    ConversationCache('slack',ts).save_msg('user',current_text)
                    log.info(f"User {user_id} in Channel {channel_id} at {ts} says: {current_text}")
                    conversations = ConversationCache('slack',ts).get_msg()
                    reply_content = SlackChannel().handle_message(conversations)
                    ConversationCache('slack',ts).save_msg('assistant',reply_content)
                    say(reply_content,thread_ts=ts)
                    log.info(f"Bot replies in Channel {channel_id} at {ts}: {reply_content}")
                else:
                    if current_text.split(' ')[0] == f'<@{bot_id}>':
                        log.info(f"User {user_id} in Channel {channel_id} says: {current_text}")
                        remove_at_text = current_text.replace(f'<@{bot_id}>','').replace(' ','')
                        modify_text = current_text.replace(f'<@{bot_id}>','')
                        if remove_at_text == '':
                            say('Hi,什么事？',thread_ts=ts)
                        else:
                            ConversationCache('slack',ts).save_msg('user',modify_text)
                            log.info(f"User {user_id} in Channel {ts} says: {modify_text}")
                            conversations = ConversationCache('slack',ts).get_msg()
                            reply_content = SlackChannel().handle_message(conversations)
                            ConversationCache('slack',ts).save_msg('assistant',reply_content)
                            log.info(f"Bot replies in Channel {channel_id} at {ts}: {reply_content}")
                            say(reply_content,thread_ts=ts)
                    else:
                        return
            else:
                return



      

      


@app.event("app_mention")
def handle_mention(body, say):
    return


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
