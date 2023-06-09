import openai
from common.base import load_config,log



class OpenAIModel:
    def __init__(self):
        self.__config = load_config()
        openai.api_key = self.__config['model']['openai']['api_key']
        proxy = self.__config['proxy']
        if proxy:
            openai.proxy = proxy
        
    def reply(self,conversation_context):
        try:
            response = openai.ChatCompletion.create(
                model = self.__config['model']['openai']['model'],
                messages = conversation_context,
                temperature = self.__config['model']['openai']['temperature'],
                top_p = self.__config['model']['openai']['top_p'],
                frequency_penalty = self.__config['model']['openai']['frequency_penalty'],
                presence_penalty = self.__config['model']['openai']['presence_penalty'],
            )
            reply_content = response.choices[0]['message']['content']
            return reply_content
        except openai.error.APIConnectionError as e:
            log.error(e)
            log.warning("I can't connect to the internet, please check your network connection")
            return "我连接不到网络，请稍后重试"
        except openai.error.Timeout as e:
            log.error(e)
            log.warning("I can't connect to the internet, please check your network connection")
            return "我没有收到消息，请稍后重试"
        except Exception as e:
            log.error(e)
            log.warning("I don't know what you are talking about, please ask me again")
            return "请再问我一次吧"

