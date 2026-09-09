from django.shortcuts import render
from accounts.decorators import role_required


def dashboard(request):
    return render(request, "core/dashboard.html")


@role_required("admin")
def settings_view(request):
    return render(request, "core/settings.html")
