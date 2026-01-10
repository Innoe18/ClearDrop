import os
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.enums import PNResourceType
from pubnub.models.consumer.access_manager import PNTokenResources

DEVICE_ID = os.getenv("DEVICE_ID", "CD-002")
TTL_MINUTES = 60

pnconfig = PNConfiguration()
pnconfig.publish_key = os.getenv("PUBNUB_PUBLISH_KEY")
pnconfig.subscribe_key = os.getenv("PUBNUB_SUBSCRIBE_KEY")
pnconfig.secret_key = os.getenv("PUBNUB_SECRET_KEY")
pnconfig.user_id = "cleardrop-server"
pnconfig.ssl = True

pubnub = PubNub(pnconfig)

channels = {
    f"cleardrop.telemetry.{DEVICE_ID}": PNTokenResources(read=True, write=True),
    f"cleardrop.cmd.{DEVICE_ID}": PNTokenResources(read=True)
}

envelope = pubnub.grant_token() \
    .channels(channels) \
    .ttl(TTL_MINUTES) \
    .sync()

print("\n=== PUBNUB TOKEN ===")
print(envelope.result.token)
print("===================\n")
