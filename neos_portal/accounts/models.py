"""
accounts/models.py — extends Django's built-in User with a role.

Django already gives you: secure password hashing, login/logout, session
management, and password reset. We don't rebuild any of that — we add one
thing on top: a Role, so you can approve someone's account AND decide what
they're allowed to do, in one place.
"""

from django.conf import settings
from django.db import models


class Role(models.TextChoices):
    ADMIN = "admin", "Admin"
    EDITOR = "editor", "Editor"
    VIEWER = "viewer", "Viewer"


class Profile(models.Model):
    """One-to-one extension of Django's User model. Created automatically
    for every new user (see signals below) so `request.user.profile.role`
    is always safe to access."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.VIEWER)
    is_active_employee = models.BooleanField(
        default=True,
        help_text="Turn off to block login without deleting the account or its history.",
    )

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    @property
    def can_edit(self) -> bool:
        return self.role in (Role.ADMIN, Role.EDITOR)

    @property
    def is_admin(self) -> bool:
        return self.role == Role.ADMIN
