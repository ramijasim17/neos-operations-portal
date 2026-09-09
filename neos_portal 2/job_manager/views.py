from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from .forms import JobForm
from .models import Job


def job_list(request):
    jobs = Job.objects.all()
    q = request.GET.get("q")
    if q:
        jobs = jobs.filter(job_name__icontains=q)
    return render(request, "job_manager/job_list.html", {"jobs": jobs, "total": jobs.count()})


@role_required("admin", "editor")
def job_create(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Job added.")
            return redirect("job_manager:list")
    else:
        form = JobForm()
    return render(request, "job_manager/job_form.html", {"form": form, "mode": "add"})


@role_required("admin", "editor")
def job_edit(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Saved.")
            return redirect("job_manager:list")
    else:
        form = JobForm(instance=job)
    return render(request, "job_manager/job_form.html", {"form": form, "job": job, "mode": "edit"})


@role_required("admin", "editor")
def job_delete(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == "POST":
        job.delete()
        messages.success(request, "Deleted.")
        return redirect("job_manager:list")
    return render(request, "job_manager/job_confirm_delete.html", {"job": job})
