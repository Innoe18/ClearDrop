import os, time, random
from datetime import datetime, timezone
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

# ✅ NO KEYS HERE
PUB_KEY = os.getenv("PUBNUB_PUBLISH_KEY")
SUB_KEY = os.getenv("PUBNUB_SUBSCRIBE_KEY")
TOKEN = os.getenv("PUBNUB_TOKEN")

CHANNEL = os.getenv("PUBNUB_TELEMETRY_CHANNEL", "cleardrop.telemetry.CD-001")

if not all([PUB_KEY, SUB_KEY, TOKEN]):
    raise RuntimeError("Missing PubNub environment variables")

pnconfig = PNConfiguration()
pnconfig.publish_key = PUB_KEY
pnconfig.subscribe_key = SUB_KEY
pnconfig.user_id = "cleardrop-sim"
pnconfig.ssl = True

# ✅ THIS IS THE IMPORTANT LINE
pnconfig.auth_key = TOKEN

pubnub = PubNub(pnconfig)

print(f"Publishing securely to {CHANNEL}")

while True:
    msg = {
        "device_id": "CD-001",
        "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "temp_c": round(random.uniform(34.0, 42.0), 1),
        "tds_ppm": int(random.uniform(80, 450)),
    }

    result = pubnub.publish().channel(CHANNEL).message(msg).sync()
    print("published:", msg, "status:", result.status.category.name)
    time.sleep(2)
