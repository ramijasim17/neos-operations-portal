from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("equipment/", include("equipment.urls")),
    path("maintenance/", include("maintenance.urls")),
    path("sqb/", include("sqb.urls")),
    path("work-approval/", include("work_approval.urls")),
    path("actions/", include("action_tracker.urls")),
    path("jobs/", include("job_manager.urls")),
    path("daily-report/", include("daily_report.urls")),
    path("personnel/", include("personnel.urls")),
    path("", include("core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
