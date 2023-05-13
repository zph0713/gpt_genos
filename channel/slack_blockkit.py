


def cache_status(cache_info):
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "对话缓存状态"
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*对话总数:*\n{cache_info['conversations_count']}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*对话长度:*\n{cache_info['conversations_length']}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*用户对话数:*\n{cache_info['user_conversations_count']}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*机器人对话数:*\n{cache_info['assistant_conversations_count']}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*系统对话数:*\n{cache_info['system_conversations_count']}"
                }
            ]
        }
    ]
    return {
        "blocks": blocks
    }


def reply_message(reply_content):
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": reply_content
            }
        }
    ]
    return {
        "blocks": blocks
    }