# app/routes/api.py
from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.models import Telemetry

api_bp = Blueprint("api", __name__, url_prefix="/api")

def telemetry_to_dict(t: Telemetry):
    return {
        "device_id": t.device_id,
        "ts": t.ts.isoformat(),
        "temp_c": t.temp_c,
        "tds_ppm": t.tds_ppm,
    }

@api_bp.get("/telemetry/latest")
@login_required
def telemetry_latest():
    device_id = request.args.get("device_id", "CD-001")
    row = (
        Telemetry.query
        .filter_by(device_id=device_id)
        .order_by(Telemetry.ts.desc())
        .first()
    )
    return jsonify({"ok": True, "data": telemetry_to_dict(row) if row else None})

@api_bp.get("/telemetry/history")
@login_required
def telemetry_history():
    device_id = request.args.get("device_id", "CD-001")
    limit = int(request.args.get("limit", "200"))
    limit = max(10, min(limit, 1000))

    rows = (
        Telemetry.query
        .filter_by(device_id=device_id)
        .order_by(Telemetry.ts.desc())
        .limit(limit)
        .all()
    )
    # return oldest → newest for charting
    rows = list(reversed(rows))
    return jsonify({"ok": True, "data": [telemetry_to_dict(r) for r in rows]})
