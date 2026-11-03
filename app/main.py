from functools import wraps
import os

from flask import Flask, jsonify, render_template, request, session

PORT = int(os.getenv("PORT", "8080"))

from app.service import (
    add_usage_record,
    authenticate_user,
    get_audits,
    get_dashboard_summary,
    get_usage_records,
    record_audit,
)

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "kyma-demo-secret")


def require_roles(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = session.get("user")
            if not user:
                return jsonify({"error": "authentication required"}), 401
            if allowed_roles and user.get("role") not in allowed_roles:
                return jsonify({"error": "forbidden"}), 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "ai-resource-impact-monitor"})


@app.post("/api/v1/login")
def login():
    payload = request.get_json(silent=True) or {}
    username = payload.get("username")
    password = payload.get("password")

    user = authenticate_user(username, password)
    if not user:
        return jsonify({"error": "invalid credentials"}), 401

    session["user"] = user
    record_audit(user["username"], "login", "auth", f"{user['username']} logged in")
    return jsonify({"message": "login successful", "user": user})


@app.post("/api/v1/logout")
def logout():
    user = session.get("user")
    if user:
        record_audit(user["username"], "logout", "auth", f"{user['username']} logged out")
    session.clear()
    return jsonify({"message": "logged out"})


@app.get("/api/v1/dashboard")
@require_roles("viewer", "analyst", "admin")
def dashboard():
    return jsonify(get_dashboard_summary())


@app.get("/api/v1/usage")
@require_roles("viewer", "analyst", "admin")
def usage():
    return jsonify({"usage_events": get_usage_records()})


@app.post("/api/v1/usage")
@require_roles("analyst", "admin")
def create_usage():
    payload = request.get_json(silent=True) or {}
    record = add_usage_record(payload)
    user = session["user"]
    record_audit(user["username"], "create", "ai_usage", f"Created usage event {record['id']}")
    return jsonify({"message": "usage record created", "record": record}), 201


@app.get("/api/v1/audits")
@require_roles("admin", "analyst")
def audits():
    return jsonify({"audit_events": get_audits()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
