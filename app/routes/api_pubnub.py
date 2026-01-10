from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Device
from app.pubnub_client import get_pubnub_server

pubnub_bp = Blueprint("pubnub_api", __name__, url_prefix="/api/pubnub")

@pubnub_bp.post("/token")
@login_required
def mint_token():
    device_id = request.json.get("device_id")
    if not device_id:
        return jsonify({"ok": False, "error": "device_id required"}), 400

    # Ensure user owns this device
    dev = Device.query.filter_by(device_id=device_id, owner_id=current_user.id).first()
    if not dev:
        return jsonify({"ok": False, "error": "device not found"}), 404

    telemetry_ch = f"cleardrop.telemetry.{device_id}"
    cmd_ch = f"cleardrop.cmd.{device_id}"

    pubnub = get_pubnub_server()

    # PAM v3 token: allow device to publish telemetry + subscribe to commands
    envelope = pubnub.grant_token() \
        .ttl(60) \
        .authorized_uuid(device_id) \
        .channels({
            telemetry_ch: {"write": True, "read": False},
            cmd_ch: {"read": True, "write": False},
        }) \
        .sync()

    token = envelope.result.token
    return jsonify({"ok": True, "token": token, "ttl_minutes": 60})
