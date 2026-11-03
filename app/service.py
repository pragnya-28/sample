from datetime import datetime, timezone

from app.mock_data import append_audit_event, append_usage_event, get_audit_log, get_usage_events, get_users


def authenticate_user(username: str, password: str):
    user = get_users().get(username)
    if user and user["password"] == password:
        return {
            "username": user["username"],
            "role": user["role"],
            "team": user["team"],
        }
    return None


def calculate_impact(event: dict) -> dict:
    compute_hours = float(event.get("compute_hours", 0))
    tokens = int(event.get("tokens", 0))
    requests = int(event.get("requests", 0))

    electricity_kwh = compute_hours * 2.1
    water_liters = compute_hours * 18.5
    carbon_kg = electricity_kwh * 0.38
    impact_index = round((tokens / 100000) + (carbon_kg / 6) + (water_liters / 1000), 2)

    return {
        "requests": requests,
        "tokens": tokens,
        "compute_hours": round(compute_hours, 2),
        "electricity_kwh": round(electricity_kwh, 2),
        "water_liters": round(water_liters, 2),
        "carbon_kg": round(carbon_kg, 2),
        "resource_impact_index": impact_index,
        "source": event.get("source"),
        "model": event.get("model"),
    }


def summarize_usage(events):
    total_requests = sum(int(event.get("requests", 0)) for event in events)
    total_tokens = sum(int(event.get("tokens", 0)) for event in events)
    total_compute_hours = sum(float(event.get("compute_hours", 0)) for event in events)

    impact_rows = [calculate_impact(event) for event in events]
    total_electricity = sum(row["electricity_kwh"] for row in impact_rows)
    total_water = sum(row["water_liters"] for row in impact_rows)
    total_carbon = sum(row["carbon_kg"] for row in impact_rows)
    highest_impact = max(impact_rows, key=lambda row: row["resource_impact_index"], default={})

    return {
        "total_requests": total_requests,
        "total_tokens": total_tokens,
        "total_compute_hours": round(total_compute_hours, 2),
        "estimated_electricity_kwh": round(total_electricity, 2),
        "estimated_water_liters": round(total_water, 2),
        "estimated_carbon_kg": round(total_carbon, 2),
        "resource_exhaustion_index": round(
            sum(row["resource_impact_index"] for row in impact_rows), 2
        ),
        "highest_impact_source": highest_impact.get("source"),
        "highest_impact_model": highest_impact.get("model"),
    }


def get_dashboard_summary():
    events = get_usage_events()
    summary = summarize_usage(events)
    by_source = {}
    for event in events:
        key = event.get("source")
        by_source[key] = by_source.get(key, 0) + int(event.get("requests", 0))

    return {
        "summary": summary,
        "top_sources": sorted(by_source.items(), key=lambda item: item[1], reverse=True),
        "usage_events": events,
    }


def get_usage_records():
    return get_usage_events()


def add_usage_record(record: dict):
    event = {
        "id": record.get("id", f"usage-{int(datetime.now(timezone.utc).timestamp())}"),
        "source": record.get("source", "unknown"),
        "team": record.get("team", "unknown"),
        "project": record.get("project", "unknown"),
        "model": record.get("model", "unknown"),
        "requests": int(record.get("requests", 0)),
        "tokens": int(record.get("tokens", 0)),
        "compute_hours": float(record.get("compute_hours", 0)),
        "region": record.get("region", "unknown"),
        "timestamp": record.get("timestamp") or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": record.get("status", "success"),
    }
    append_usage_event(event)
    return event


def get_audits():
    return get_audit_log()


def record_audit(user: str, action: str, resource: str, details: str):
    event = {
        "id": f"audit-{int(datetime.now(timezone.utc).timestamp())}",
        "user": user,
        "action": action,
        "resource": resource,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "details": details,
    }
    append_audit_event(event)
    return event
