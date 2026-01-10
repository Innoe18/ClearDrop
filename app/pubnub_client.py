import os
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub


def get_pubnub() -> PubNub:
    pnconfig = PNConfiguration()
    pnconfig.publish_key = os.getenv("PUBNUB_PUBLISH_KEY")
    pnconfig.subscribe_key = os.getenv("PUBNUB_SUBSCRIBE_KEY")
    pnconfig.secret_key = os.getenv("PUBNUB_SECRET_KEY")
    pnconfig.user_id = os.getenv("PUBNUB_USER_ID", "cleardrop-server")
    pnconfig.ssl = True
    return PubNub(pnconfig)


def get_pubnub_server() -> PubNub:
    return get_pubnub()
