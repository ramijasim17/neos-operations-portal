from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from .forms import ApprovalRecordForm
from .models import ApprovalRecord, FileType, DEFAULT_TYPES


def _ensure_default_types():
    if not FileType.objects.exists():
        for name in DEFAULT_TYPES:
            FileType.objects.get_or_create(name=name)


def record_list(request):
    _ensure_default_types()
    records = ApprovalRecord.objects.select_related("file_type").all()

    q = request.GET.get("q")
    file_type = request.GET.get("file_type")
    status = request.GET.get("status")

    if q:
        records = records.filter(details__icontains=q)
    if file_type:
        records = records.filter(file_type__name=file_type)

    rows = list(records)
    if status:
        rows = [r for r in rows if r.status == status]

    counts = {"expired": 0, "soon": 0, "valid": 0}
    for r in records:
        if r.status in counts:
            counts[r.status] += 1

    return render(request, "work_approval/record_list.html", {
        "rows": rows, "counts": counts, "total": records.count(),
        "file_types": FileType.objects.all(),
    })


@role_required("admin", "editor")
def record_create(request):
    _ensure_default_types()
    if request.method == "POST":
        form = ApprovalRecordForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.uploaded_by = request.user
            obj.save()
            messages.success(request, "Record added.")
            return redirect("work_approval:list")
    else:
        form = ApprovalRecordForm()
    return render(request, "work_approval/record_form.html", {"form": form, "mode": "add"})


@role_required("admin", "editor")
def record_edit(request, record_id):
    record = get_object_or_404(ApprovalRecord, id=record_id)
    if request.method == "POST":
        form = ApprovalRecordForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.uploaded_by = request.user
            obj.save()
            messages.success(request, "Saved.")
            return redirect("work_approval:list")
    else:
        form = ApprovalRecordForm(instance=record)
    return render(request, "work_approval/record_form.html", {"form": form, "record": record, "mode": "edit"})


@role_required("admin", "editor")
def record_delete(request, record_id):
    record = get_object_or_404(ApprovalRecord, id=record_id)
    if request.method == "POST":
        record.delete()
        messages.success(request, "Deleted.")
        return redirect("work_approval:list")
    return render(request, "work_approval/record_confirm_delete.html", {"record": record})


@role_required("admin")
def manage_types(request):
    if request.method == "POST":
        if "add" in request.POST:
            name = request.POST.get("new_type", "").strip()
            if name:
                FileType.objects.get_or_create(name=name)
                messages.success(request, f"Added: {name}")
        elif "delete" in request.POST:
            FileType.objects.filter(id=request.POST.get("delete")).delete()
            messages.success(request, "Deleted.")
        return redirect("work_approval:manage_types")
    return render(request, "work_approval/manage_types.html", {"file_types": FileType.objects.all()})
