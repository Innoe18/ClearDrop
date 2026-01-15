import os
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

device_id = os.getenv("DEVICE_ID")
if not device_id:
    raise SystemExit("Set DEVICE_ID first, e.g. export DEVICE_ID=CD-002")

PUB = os.getenv("PUBNUB_PUBLISH_KEY")
SUB = os.getenv("PUBNUB_SUBSCRIBE_KEY")
SEC = os.getenv("PUBNUB_SECRET_KEY")

missing = [k for k,v in [("PUBNUB_PUBLISH_KEY",PUB),("PUBNUB_SUBSCRIBE_KEY",SUB),("PUBNUB_SECRET_KEY",SEC)] if not v]
if missing:
    raise SystemExit(f"Missing env vars: {', '.join(missing)}")

telemetry_chan = f"cleardrop.telemetry.{device_id}"
cmd_chan = f"cleardrop.cmd.{device_id}"

pnconfig = PNConfiguration()
pnconfig.publish_key = PUB
pnconfig.subscribe_key = SUB
pnconfig.secret_key = SEC
pnconfig.user_id = "cleardrop-admin"
pnconfig.ssl = True

pubnub = PubNub(pnconfig)


envelope = pubnub.grant() \
    .channels([telemetry_chan, cmd_chan]) \
    .auth_keys([device_id]) \
    .read(True) \
    .write(True) \
    .ttl(60) \
    .sync()

print("Granted for auth_key:", device_id)
print("Channels:", telemetry_chan, cmd_chan)
print("Status:", envelope.status.status_code, envelope.status.category)
