import os
import json
import time

class ConversationCache:
    def __init__(self,channel_type,conversation_id):
        self.cache = []
        self.cache_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cache', channel_type)
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)
        self.cache_file = os.path.join(self.cache_path,conversation_id + '.json')
        
    

    