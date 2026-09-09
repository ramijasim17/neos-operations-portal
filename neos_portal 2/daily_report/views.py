from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from .forms import DailyReportForm
from .models import DailyReport


def report_list(request):
    reports = DailyReport.objects.all()
    q = request.GET.get("q")
    if q:
        reports = reports.filter(job_name__icontains=q)
    return render(request, "daily_report/report_list.html", {"reports": reports, "total": reports.count()})


@role_required("admin", "editor")
def report_create(request):
    if request.method == "POST":
        form = DailyReportForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Report added.")
            return redirect("daily_report:list")
    else:
        form = DailyReportForm()
    return render(request, "daily_report/report_form.html", {"form": form, "mode": "add"})


@role_required("admin", "editor")
def report_edit(request, report_id):
    report = get_object_or_404(DailyReport, id=report_id)
    if request.method == "POST":
        form = DailyReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, "Saved.")
            return redirect("daily_report:list")
    else:
        form = DailyReportForm(instance=report)
    return render(request, "daily_report/report_form.html", {"form": form, "report": report, "mode": "edit"})


@role_required("admin", "editor")
def report_delete(request, report_id):
    report = get_object_or_404(DailyReport, id=report_id)
    if request.method == "POST":
        report.delete()
        messages.success(request, "Deleted.")
        return redirect("daily_report:list")
    return render(request, "daily_report/report_confirm_delete.html", {"report": report})
