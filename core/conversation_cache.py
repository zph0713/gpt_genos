from common.base import log

conversation_cache = {}

class ConversationCache:
    def __init__(self,channel_type,conversation_id):
        self.channel_type = channel_type
        self.conversation_id = conversation_id
        try:
            self.channel = conversation_cache[self.channel_type]
        except KeyError:
            conversation_cache[self.channel_type] = {}
            self.channel = conversation_cache[self.channel_type]
        
    def save_msg(self,role,content):
        try:
            msg_cache = self.channel[self.conversation_id]
        except KeyError:
            self.channel[self.conversation_id] = []
            msg_cache = self.channel[self.conversation_id]
            log.info(f"创建新的缓存消息列表：{self.channel_type} {self.conversation_id}")
        msg_fmt = {
            'role': role,
            'content': content
        }
        msg_cache.append(msg_fmt)
        msg_length = sum([len(i) for i in msg_cache])
        while msg_length > 4096:
            msg_cache.pop(0)
            msg_length = sum([len(i) for i in msg_cache])
        conversation_cache[self.channel_type][self.conversation_id] = msg_cache
        log.info(f"当前的缓存消息长度为：{msg_length},当前的缓存消息数量为：{len(msg_cache)}")
    
    def get_msg(self):
        return conversation_cache[self.channel_type][self.conversation_id]