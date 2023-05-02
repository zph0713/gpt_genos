# GPT_Genos
GPT_Genos是一个用于运行slack机器人调用chatgpt进行对话的程序。
## 用途
GPT_Genos旨在为用户提供一种简单的方法，通过运行slack机器人来与chatgpt进行对话。chatgpt是一种基于OpenAI GPT-2模型的自然语言生成模型，可以生成自然流畅的文本，并且具有广泛的应用场景。
## 运行方式
要运行GPT_Genos，您需要使用Python 3，并在终端中执行以下命令：

```python3 app.py```

在程序开始运行后，您可以通过启动slack机器人来与chatgpt进行对话。您需要配置您的slack机器人的API密钥，并将其添加到您的工作区中。
## 代码结构
GPT_Genos的代码结构如下：
- ```app.py```: 程序运行文件。
- ```conf/config.json```: 配置文件，包含程序所需的各种配置信息。
- ```channel/slack_channel.py```: slack机器人类，用于与slack进行交互。
- ```models/openai_model.py```: chatgpt类，用于与chatgpt进行交互。
- ```common/selector.py```: channel和model的选择器，便于后期扩展其他。
