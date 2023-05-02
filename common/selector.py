from common.base import load_config
import channel



class ChannelSelector(object):
    def __init__(self, channel):
        self.channel = channel

    def create_channel(self):
        if self.channel == 'slack':
            from channel.slack_channel import SlackChannel
            return SlackChannel()
        else:
            raise Exception('Channel not found')
        

class ModelSelector(object):
    def __init__(self, model):
        self.model = model

    def create_model(self):
        if self.model == 'openai':
            from models.openai_model import OpenAIModel
            return OpenAIModel()
        else:
            raise Exception('Model not found')
