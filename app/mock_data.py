USERS = {
    "ops-admin": {
        "username": "ops-admin",
        "password": "admin123",
        "role": "admin",
        "team": "platform-operations",
    },
    "ai-analyst": {
        "username": "ai-analyst",
        "password": "analyst123",
        "role": "analyst",
        "team": "data-platform",
    },
    "viewer": {
        "username": "viewer",
        "password": "viewer123",
        "role": "viewer",
        "team": "platform-readonly",
    },
}

USAGE_EVENTS = [
    {
        "id": "usage-1001",
        "source": "openai",
        "team": "data-platform",
        "project": "support-bot",
        "model": "gpt-4o-mini",
        "requests": 2040,
        "tokens": 820000,
        "compute_hours": 18.4,
        "region": "us-east-1",
        "timestamp": "2026-11-03T09:00:00Z",
        "status": "success",
    },
    {
        "id": "usage-1002",
        "source": "azure-openai",
        "team": "research",
        "project": "diagnostics-rag",
        "model": "gpt-4o",
        "requests": 870,
        "tokens": 430000,
        "compute_hours": 10.2,
        "region": "eu-central-1",
        "timestamp": "2026-11-03T10:15:00Z",
        "status": "success",
    },
    {
        "id": "usage-1003",
        "source": "internal-model",
        "team": "analytics",
        "project": "log-anomaly-detection",
        "model": "llama-3.1-70b",
        "requests": 1420,
        "tokens": 510000,
        "compute_hours": 22.5,
        "region": "us-west-2",
        "timestamp": "2026-11-03T12:40:00Z",
        "status": "warning",
    },
    {
        "id": "usage-1004",
        "source": "mcp-chatbot",
        "team": "platform-operations",
        "project": "runbook-assistant",
        "model": "claude-3-sonnet",
        "requests": 600,
        "tokens": 240000,
        "compute_hours": 7.3,
        "region": "ap-southeast-1",
        "timestamp": "2026-11-03T14:20:00Z",
        "status": "success",
    },
]

AUDIT_LOG = [
    {
        "id": "audit-1000",
        "user": "ops-admin",
        "action": "login",
        "resource": "auth",
        "timestamp": "2026-11-03T08:00:00Z",
        "details": "Admin user signed in to the AI resource monitor.",
    }
]


def get_users():
    return USERS


def get_usage_events():
    return USAGE_EVENTS


def append_usage_event(event):
    USAGE_EVENTS.append(event)


def get_audit_log():
    return AUDIT_LOG


def append_audit_event(event):
    AUDIT_LOG.append(event)
