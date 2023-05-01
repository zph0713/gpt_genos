import json
import os



## load上级目录下的conf目录下的config.json
def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'conf', 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

if __name__ == '__main__':
    print(load_config())