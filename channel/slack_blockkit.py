


def cache_status(cache_info):
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Conversation Cache Status"
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Conversations Count:*\n{cache_info['conversations_count']}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Conversations Length:*\n{cache_info['conversations_length']}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*User Conversations Count:*\n{cache_info['user_conversations_count']}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Assistant Conversations Count:*\n{cache_info['assistant_conversations_count']}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*System Conversations Count:*\n{cache_info['system_conversations_count']}"
                }
            ]
        }
    ]
    return {
        "blocks": blocks
    }