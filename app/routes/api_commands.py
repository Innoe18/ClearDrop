from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

from app.models import Device
from app.pubnub_client import get_pubnub

cmd_bp = Blueprint("cmd", __name__, url_prefix="/api")


def cmd_channel(device_id: str) -> str:
    return f"cleardrop.cmd.{device_id}"


@cmd_bp.post("/device/<device_id>/command")
@login_required
def send_command(device_id):
    # Ensure user owns the device
    dev = Device.query.filter_by(
        device_id=device_id,
        owner_id=current_user.id
    ).first()

    if not dev:
        return jsonify({"ok": False, "error": "Device not found"}), 404

    payload = request.get_json(silent=True) or {}
    cmd = payload.get("cmd")

    if cmd not in {"buzz", "stop"}:
        return jsonify({"ok": False, "error": "Invalid command"}), 400

    message = {
        "cmd": cmd,
        "pattern": payload.get("pattern", "beep"),
        "freq_hz": int(payload.get("freq_hz", 1000)),
        "duration_ms": int(payload.get("duration_ms", 800)),
    }

    pubnub = get_pubnub()
    pubnub.publish().channel(cmd_channel(device_id)).message(message).sync()

    return jsonify({"ok": True, "sent": message})
