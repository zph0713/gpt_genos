import os
import json
import time


conversation_cache = {}

class ConversationCache:
    def __init__(self,channel_type,conversation_id):
        self.channel_type = channel_type
        self.conversation_id = conversation_id
        
    def save_msg(self,message):
        self.cache.append(message)
    
    def get_cache_msg(self):
        return conversation_cache[self.channel_type][self.conversation_id]