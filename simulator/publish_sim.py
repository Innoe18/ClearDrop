import os, time, random
from datetime import datetime, timezone
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

PUB_KEY = os.getenv("PUBNUB_PUBLISH_KEY")
SUB_KEY = os.getenv("PUBNUB_SUBSCRIBE_KEY")
CHANNEL = os.getenv("PUBNUB_TELEMETRY_CHANNEL", "cleardrop.telemetry.CD-001")

pnconfig = PNConfiguration()
pnconfig.publish_key = PUB_KEY
pnconfig.subscribe_key = SUB_KEY
pnconfig.user_id = "cleardrop-sim"
pnconfig.ssl = True

pubnub = PubNub(pnconfig)

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
