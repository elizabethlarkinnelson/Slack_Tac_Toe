import os
from slackclient import SlackClient

SLACK_TOKEN = os.environ.get('SLACK_TOKEN_KEY')
slack_client = SlackClient(SLACK_TOKEN)


def list_channels():
    channels_call = slack_client.api_call("channels.list")
    if channels_call.get("ok"):
        return channels_call['channels']
    return None


if __name__ == "__main__":
    channels = list_channels()
    if channels:
        print "Channels: "
        for c in channels:
            print c['name'] + " ( " + c['id'] + ")"
    else:
        print("Unable to authenticate.")
