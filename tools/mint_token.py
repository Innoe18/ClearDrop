import os
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.models.consumer.access_manager import Space


def must(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise SystemExit(f"Missing env var: {name}")
    return v


PUB = must("PUBNUB_PUBLISH_KEY")
SUB = must("PUBNUB_SUBSCRIBE_KEY")
SECRET = must("PUBNUB_SECRET_KEY")

DEVICE_ID = os.getenv("DEVICE_ID", "CD-001")
TTL_MINUTES = int(os.getenv("TTL_MINUTES", "60"))


telemetry_ch = f"cleardrop.telemetry.{DEVICE_ID}"
cmd_ch = f"cleardrop.cmd.{DEVICE_ID}"

pnconfig = PNConfiguration()
pnconfig.publish_key = PUB
pnconfig.subscribe_key = SUB
pnconfig.secret_key = SECRET
pnconfig.user_id = "cleardrop-admin"
pnconfig.ssl = True

pubnub = PubNub(pnconfig)


spaces = [
    Space.id(telemetry_ch).write(),
    Space.id(cmd_ch).read()
]

envelope = (
    pubnub.grant_token()
    .spaces(spaces)
    .ttl(TTL_MINUTES)
    .authorized_user(DEVICE_ID)  
    .sync()
)


print(envelope.result.token)
