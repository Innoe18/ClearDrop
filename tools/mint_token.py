import os
import sys
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

DEVICE_ID = os.getenv("DEVICE_ID", "CD-001")
TTL_MINUTES = int(os.getenv("TTL_MINUTES", "1440"))  # 24h default

PUB_KEY = os.getenv("PUBNUB_PUBLISH_KEY")
SUB_KEY = os.getenv("PUBNUB_SUBSCRIBE_KEY")
SECRET = os.getenv("PUBNUB_SECRET_KEY")

if not (PUB_KEY and SUB_KEY and SECRET):
    print("Missing env vars. Need PUBNUB_PUBLISH_KEY, PUBNUB_SUBSCRIBE_KEY, PUBNUB_SECRET_KEY", file=sys.stderr)
    sys.exit(1)

# Channels your device needs:
telemetry_ch = f"cleardrop.telemetry.{DEVICE_ID}"
cmd_ch = f"cleardrop.cmd.{DEVICE_ID}"

pnconfig = PNConfiguration()
pnconfig.publish_key = PUB_KEY
pnconfig.subscribe_key = SUB_KEY
pnconfig.secret_key = SECRET
pnconfig.user_id = "cleardrop-token-minter"
pnconfig.ssl = True

pubnub = PubNub(pnconfig)

resources = {
    "channels": {
        telemetry_ch: {"read": True, "write": True},  # device can pub/sub its telemetry channel
        cmd_ch: {"read": True, "write": False},       # device can READ commands, not write them
    },
    "uuids": {},
    "groups": {},
}

patterns = {"channels": {}, "uuids": {}, "groups": {}}

# Some SDK versions use .authorized_uuid(), others .authorized_user_id()
builder = pubnub.grant_token().ttl(TTL_MINUTES).resources(resources).patterns(patterns)

if hasattr(builder, "authorized_uuid"):
    builder = builder.authorized_uuid(DEVICE_ID)
elif hasattr(builder, "authorized_user_id"):
    builder = builder.authorized_user_id(DEVICE_ID)

envelope = builder.sync()

token = getattr(envelope.result, "token", None) if hasattr(envelope, "result") else None
if not token and isinstance(envelope, dict):
    token = envelope.get("token")

if not token:
    print("Could not read token from response:", envelope, file=sys.stderr)
    sys.exit(2)

print(token)
