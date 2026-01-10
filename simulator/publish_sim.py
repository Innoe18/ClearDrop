import os, time, random
from datetime import datetime, timezone
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

PUB_KEY = os.getenv("PUBNUB_PUBLISH_KEY")
SUB_KEY = os.getenv("PUBNUB_SUBSCRIBE_KEY")

DEVICE_ID = os.getenv("DEVICE_ID", "CD-001")
CHANNEL = os.getenv("CHANNEL", f"cleardrop.telemetry.{DEVICE_ID}")

if not PUB_KEY or not SUB_KEY:
    raise SystemExit("Missing PUBNUB_PUBLISH_KEY or PUBNUB_SUBSCRIBE_KEY in env")

pnconfig = PNConfiguration()
pnconfig.publish_key = PUB_KEY
pnconfig.subscribe_key = SUB_KEY
pnconfig.user_id = os.getenv("PUBNUB_USER_ID", "cleardrop-sim")
pnconfig.ssl = True

pubnub = PubNub(pnconfig)

print(f"Publishing as {DEVICE_ID} on {CHANNEL}")

while True:
    msg = {
        "device_id": DEVICE_ID,
        "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "temp_c": round(random.uniform(34.0, 42.0), 1),
        "tds_ppm": int(random.uniform(80, 450)),
    }
    result = pubnub.publish().channel(CHANNEL).message(msg).sync()
    print("published:", msg, "status:", result.status.category.name)
    time.sleep(2)
