from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Device

dash_bp = Blueprint("dash", __name__)

@dash_bp.route("/")
def home():
    return redirect(url_for("dash.dashboard"))

@dash_bp.route("/dashboard")
@login_required
def dashboard():
    devices = Device.query.filter_by(owner_id=current_user.id).all()

    # device_id can come from URL: /dashboard?device_id=CD-001
    selected_device_id = request.args.get("device_id")

    # If no device_id provided, default to user's first device (if any)
    if not selected_device_id and devices:
        selected_device_id = devices[0].device_id

    return render_template(
        "dashboard.html",
        devices=devices,
        device_id=selected_device_id
    )

@dash_bp.route("/devices", methods=["GET", "POST"])
@login_required
def devices():
    if request.method == "POST":
        device_id = request.form.get("device_id", "").strip()
        nickname = request.form.get("nickname", "").strip() or "My ClearDrop"

        if not device_id:
            flash("Device ID is required.", "danger")
            return redirect(url_for("dash.devices"))

        existing = Device.query.filter_by(device_id=device_id).first()
        if existing:
            flash("That Device ID is already registered.", "warning")
            return redirect(url_for("dash.devices"))

        dev = Device(device_id=device_id, nickname=nickname, owner_id=current_user.id)
        db.session.add(dev)
        db.session.commit()
        flash("Device added!", "success")
        return redirect(url_for("dash.dashboard"))

    devices = Device.query.filter_by(owner_id=current_user.id).all()
    return render_template("devices.html", devices=devices)
