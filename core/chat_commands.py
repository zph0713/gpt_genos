from core.conversation_cache import ConversationCache
from channel.slack_blockkit import *




class chat_commands(object):
    def __init__(self, channel_type, channel_id, conversation_id, current_text):
        self.channel_type = channel_type
        self.channel_id = channel_id
        self.conversation_id = conversation_id
        self.current_text = current_text
        self.commands = {
            '#help': 'help',
            '#version': 'version',
            '#cacheinfo': 'cacheinfo',
            '#clear': 'clear'
        }

    def handle(self):
        if self.current_text.startswith('#'):
            if self.current_text in self.commands.keys():
                return getattr(self, self.commands[self.current_text])()
            else:
                return '命令错误，请输入#help查看帮助'
        else:
            return self.current_text
        
    def help(self):
        return '输入#clear清空对话，输入#cacheinfo查看cache信息，输入#help查看帮助'
    
    def version(self):
        return '当前版本为0.0.1'
    
    def cacheinfo(self):
        conversations = ConversationCache(self.channel_type,self.conversation_id).get_msg()
        cache_info = {
            'conversations_count': len(conversations),
            'conversations_length': sum([len(str(i)) for i in conversations]),
            'user_conversations_count': len([i for i in conversations if i['role'] == 'user']),
            'assistant_conversations_count': len([i for i in conversations if i['role'] == 'assistant']),
            'system_conversations_count': len([i for i in conversations if i['role'] == 'system'])
        }
        return cache_status(cache_info)
    
    def clear(self):
        ConversationCache(self.channel_type,self.conversation_id).clear_msg()
        return '对话已清空'
    