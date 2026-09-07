"""Makes the sidebar navigation list available to every template, built
from the user's role — this is where 'different people see different tabs'
actually happens, in one place rather than scattered per-page checks."""

NAV_ITEMS = [
    {"label": "Equipment",           "url_name": "equipment:list",       "roles": ("admin", "editor", "viewer")},
    {"label": "Certificates",        "url_name": "equipment:cert_list",  "roles": ("admin", "editor", "viewer")},
    # Maintenance, SQB, Work Approval & SOC, Action Tracker, Personnel,
    # Job Manager, and Daily Report follow the same pattern once their
    # apps are built — add their entries here.
    {"label": "Settings & Sync",     "url_name": "core:settings",        "roles": ("admin",)},
]


def nav_items(request):
    if not request.user.is_authenticated:
        return {}
    profile = getattr(request.user, "profile", None)
    role = profile.role if profile else "viewer"
    visible = [item for item in NAV_ITEMS if role in item["roles"]]
    return {"nav_items": visible, "user_role": role}
