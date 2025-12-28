import os
from datetime import datetime
from threading import Thread

from pubnub.callbacks import SubscribeCallback
from pubnub.pubnub import PubNub

from app import db
from app.models import Telemetry
from app.pubnub_client import get_pubnub


def _parse_ts(ts: str | None) -> datetime | None:
    if not ts:
        return None
    try:
        # Accept ISO string with Z
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).replace(tzinfo=None)
    except Exception:
        return None


class TelemetryListener(SubscribeCallback):
    def __init__(self, flask_app):
        self.flask_app = flask_app

    def message(self, pubnub: PubNub, event):
        msg = event.message

        # PubNub usually delivers dicts, but handle strings just in case
        if not isinstance(msg, dict):
            return

        device_id = msg.get("device_id")
        temp_c = msg.get("temp_c")
        tds_ppm = msg.get("tds_ppm")

        if not device_id or temp_c is None or tds_ppm is None:
            return

        ts = _parse_ts(msg.get("ts"))

        with self.flask_app.app_context():
            row = Telemetry(
                device_id=str(device_id),
                temp_c=float(temp_c),
                tds_ppm=int(tds_ppm),
            )
            if ts:
                row.ts = ts
            db.session.add(row)
            db.session.commit()

def start_iot_worker(flask_app):
    channel = os.getenv("PUBNUB_TELEMETRY_CHANNEL", "cleardrop.telemetry.CD-001")
    pubnub = get_pubnub()
    pubnub.add_listener(TelemetryListener(flask_app))
    pubnub.subscribe().channels([channel]).execute()

    # keep a daemon thread alive (pubnub uses background threads)
    def _keep_alive():
        import time
        while True:
            time.sleep(60)

    Thread(target=_keep_alive, daemon=True).start()
