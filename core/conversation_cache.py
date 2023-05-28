from common.base import log
from common.caches import RedisCache




class ConversationCache(object):
    def __init__(self,channel_type,conversation_id):
        self.channel_type = channel_type
        self.conversation_id = conversation_id
        self.cache = RedisCache()
        self.channel = self.cache.get(self.channel_type)
        if self.channel == None:
            self.cache.set(self.channel_type, {})
            self.channel = self.cache.get(self.channel_type)
        
    def save_msg(self,role,content,user=None):
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
        if user:
            msg_fmt['user'] = user
        msg_cache.append(msg_fmt)
        msg_length = sum([len(str(i)) for i in msg_cache])
        while msg_length > 4096:
            msg_cache.pop(0)
            msg_length = sum([len(str(i)) for i in msg_cache])
        self.channel[self.conversation_id] = msg_cache
        self.cache.set(self.channel_type, self.channel)
        log.info(f"当前的缓存消息长度为：{msg_length},当前的缓存消息数量为：{len(msg_cache)}")
    
    def get_msg(self):
        return self.channel[self.conversation_id]
    
    def clear_msg(self):
        self.channel[self.conversation_id] = []
        self.cache.set(self.channel_type, self.channel)
        log.info(f"清空缓存消息：{self.channel_type} {self.conversation_id}")