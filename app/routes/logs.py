from datetime import datetime
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models import Device, Telemetry

logs_bp = Blueprint("logs", __name__)


@logs_bp.route("/logs")
@login_required
def logs():
    # device dropdown
    devices = Device.query.filter_by(owner_id=current_user.id).all()
    selected_device = request.args.get("device_id") or (devices[0].device_id if devices else None)

    limit = int(request.args.get("limit", "200"))
    limit = max(10, min(limit, 1000))

    q = Telemetry.query
    if selected_device:
        q = q.filter_by(device_id=selected_device)

    rows = q.order_by(Telemetry.ts.desc()).limit(limit).all()

    return render_template(
        "logs.html",
        devices=devices,
        selected_device=selected_device,
        rows=rows,
        limit=limit
    )
