"""
LoginRequiredMiddleware — this is the actual "control access" mechanism.

By default, EVERY view in the portal requires a logged-in, active account.
Instead of remembering to add @login_required to every single view (easy
to forget on one and accidentally leave a page public), this middleware
makes "logged in" the default and lets you explicitly opt individual paths
OUT via the prefix list below — e.g. the login page itself, and Django's
password-reset flow, both of which have to be reachable by someone who
isn't logged in yet.

Note: this deliberately checks request.path against fixed prefixes, NOT
request.resolver_match — resolver_match isn't populated yet at the point
this middleware's __call__ runs (it's set later, right before the view
itself executes), so checking it here always returns None. That bug, if
shipped, would have made the login page redirect to itself in an infinite
loop, locking every single user out. Caught by testing before deploy.
"""

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.urls import reverse

EXEMPT_PATH_PREFIXES = (
    "/accounts/login",
    "/accounts/password-reset",
    "/accounts/reset/",
)


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        is_exempt = (
            any(path.startswith(p) for p in EXEMPT_PATH_PREFIXES)
            or path.startswith("/admin/")
            or path.startswith(settings.STATIC_URL)
        )

        if not request.user.is_authenticated:
            if not is_exempt:
                return redirect_to_login(request.get_full_path(), login_url=reverse("accounts:login"))

        elif not is_exempt and (
            not getattr(request.user, "profile", None) or not request.user.profile.is_active_employee
        ):
            # A real Django account that's been deactivated in Profile
            # (e.g. someone who left the company) — logged out immediately,
            # rather than just hidden behind a permission check that a
            # future developer might forget to add somewhere.
            from django.contrib.auth import logout
            logout(request)
            return redirect_to_login(request.get_full_path(), login_url=reverse("accounts:login"))

        return self.get_response(request)
