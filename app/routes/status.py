from datetime import datetime, timezone
from flask import Blueprint, jsonify, render_template
from flask_login import login_required
from app.models import Telemetry

status_bp = Blueprint("status", __name__)

@status_bp.route("/status")
@login_required
def status_page():
    return render_template("status.html")

@status_bp.route("/api/status")
@login_required
def status_api():
    last = Telemetry.query.order_by(Telemetry.ts.desc()).first()
    return jsonify({
        "ok": True,
        "server_time": datetime.now(timezone.utc).isoformat(),
        "last_telemetry_ts": last.ts.isoformat() if last else None,
        "last_telemetry_device": last.device_id if last else None,
    })
