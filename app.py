import signal
from multiprocessing import Pool
from core.selector import ChannelSelector
from common.base import load_config,log


def start_channel(channel_type):
    log.info(f"Starting {channel_type} channel...")
    channel = ChannelSelector(channel_type).create_channel()
    channel.startup()

def shutdown_channel(channel_type):
    log.info(f"Shutting down {channel_type} channel...")
    channel = ChannelSelector(channel_type).create_channel()
    channel.shutdown()

signal.signal(signal.SIGINT, shutdown_channel)

def main():
    try:
        config = load_config()
        channel_list = config['type_choices']['channels']
        if len(channel_list) == 0:
            raise Exception('No channel selected')
        elif len(channel_list) == 1:
            start_channel(channel_list[0])
        else:
            pool = Pool(processes=len(channel_list))
            for channel_type in channel_list:
                pool.apply_async(start_channel, (channel_type,))
                start_channel(channel_type)
            pool.close()
            pool.join()
    except Exception as e:
        log.error(e)
        log.warning("I can't start, please check your configuration")
        print('启动失败')

if __name__ == '__main__':
    main()
