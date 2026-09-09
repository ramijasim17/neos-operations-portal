"""Makes the sidebar navigation list available to every template, built
from the user's role — this is where 'different people see different tabs'
actually happens, in one place rather than scattered per-page checks."""

NAV_ITEMS = [
    {"label": "Equipment",           "url_name": "equipment:list",       "roles": ("admin", "editor", "viewer")},
    {"label": "Certificates",        "url_name": "equipment:cert_list",  "roles": ("admin", "editor", "viewer")},
    {"label": "Maintenance",         "url_name": "maintenance:list",     "roles": ("admin", "editor", "viewer")},
    {"label": "Job Manager",         "url_name": "job_manager:list",     "roles": ("admin", "editor", "viewer")},
    {"label": "Personnel",           "url_name": "personnel:list",       "roles": ("admin", "editor", "viewer")},
    {"label": "Action Tracker",      "url_name": "action_tracker:list",  "roles": ("admin", "editor", "viewer")},
    {"label": "Daily Report",        "url_name": "daily_report:list",    "roles": ("admin", "editor", "viewer")},
    {"label": "Work Approval & SOC", "url_name": "work_approval:list",   "roles": ("admin", "editor", "viewer")},
    {"label": "SQB",                 "url_name": "sqb:list",             "roles": ("admin", "editor", "viewer")},
    {"label": "Settings & Sync",     "url_name": "core:settings",        "roles": ("admin",)},
]


def nav_items(request):
    if not request.user.is_authenticated:
        return {}
    profile = getattr(request.user, "profile", None)
    role = profile.role if profile else "viewer"

    current_view_name = None
    if getattr(request, "resolver_match", None):
        current_view_name = request.resolver_match.view_name  # e.g. "equipment:cert_list"

    visible = []
    for item in NAV_ITEMS:
        if role in item["roles"]:
            visible.append({**item, "is_active": item["url_name"] == current_view_name})

    return {"nav_items": visible, "user_role": role}
