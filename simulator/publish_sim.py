import os, time, random
from datetime import datetime, timezone
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

DEVICE_ID = os.getenv("DEVICE_ID", "CD-002")
CHANNEL = f"cleardrop.telemetry.{DEVICE_ID}"

pnconfig = PNConfiguration()
pnconfig.publish_key = os.getenv("PUBNUB_PUBLISH_KEY")
pnconfig.subscribe_key = os.getenv("PUBNUB_SUBSCRIBE_KEY")
pnconfig.user_id = f"cleardrop-sim-{DEVICE_ID}"


pnconfig.auth_key = os.getenv("PUBNUB_AUTH_KEY", DEVICE_ID)

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
