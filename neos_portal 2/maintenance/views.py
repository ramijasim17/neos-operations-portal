from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from .forms import MaintenanceRecordForm
from .models import MaintenanceLevel, MaintenanceRecord, DEFAULT_LEVELS


def _ensure_default_levels():
    if not MaintenanceLevel.objects.exists():
        for name in DEFAULT_LEVELS:
            MaintenanceLevel.objects.get_or_create(name=name)


def record_list(request):
    _ensure_default_levels()
    records = MaintenanceRecord.objects.select_related("equipment", "level").all()

    q = request.GET.get("q")
    level = request.GET.get("level")
    category = request.GET.get("category")

    if q:
        records = records.filter(equipment__serial_number__icontains=q)
    if level:
        records = records.filter(level__name=level)
    if category:
        records = records.filter(equipment__category=category)

    status = request.GET.get("status")
    rows = list(records)
    if status:
        rows = [r for r in rows if r.status == status]

    counts = {"expired": 0, "soon": 0, "valid": 0}
    for r in records:
        if r.status in counts:
            counts[r.status] += 1

    return render(request, "maintenance/record_list.html", {
        "rows": rows,
        "counts": counts,
        "total": records.count(),
        "levels": MaintenanceLevel.objects.all(),
    })


@role_required("admin", "editor")
def record_create(request):
    _ensure_default_levels()
    if request.method == "POST":
        form = MaintenanceRecordForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.uploaded_by = request.user
            obj.save()
            messages.success(request, "Maintenance record added.")
            return redirect("maintenance:list")
    else:
        form = MaintenanceRecordForm()
    return render(request, "maintenance/record_form.html", {"form": form, "mode": "add"})


@role_required("admin", "editor")
def record_edit(request, record_id):
    record = get_object_or_404(MaintenanceRecord, id=record_id)
    if request.method == "POST":
        form = MaintenanceRecordForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.uploaded_by = request.user
            obj.save()
            messages.success(request, "Saved.")
            return redirect("maintenance:list")
    else:
        form = MaintenanceRecordForm(instance=record)
    return render(request, "maintenance/record_form.html", {"form": form, "record": record, "mode": "edit"})


@role_required("admin", "editor")
def record_delete(request, record_id):
    record = get_object_or_404(MaintenanceRecord, id=record_id)
    if request.method == "POST":
        record.delete()
        messages.success(request, "Deleted.")
        return redirect("maintenance:list")
    return render(request, "maintenance/record_confirm_delete.html", {"record": record})


@role_required("admin")
def manage_levels(request):
    if request.method == "POST":
        if "add" in request.POST:
            name = request.POST.get("new_level", "").strip()
            if name:
                MaintenanceLevel.objects.get_or_create(name=name)
                messages.success(request, f"Added level: {name}")
        elif "delete" in request.POST:
            MaintenanceLevel.objects.filter(id=request.POST.get("delete")).delete()
            messages.success(request, "Level deleted.")
        return redirect("maintenance:manage_levels")

    return render(request, "maintenance/manage_levels.html", {"levels": MaintenanceLevel.objects.all()})
