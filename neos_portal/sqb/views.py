import io

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from .models import SQBJob, SQBDocument, SQB_DOCUMENT_TYPES

try:
    from pypdf import PdfWriter, PdfReader
except ImportError:
    PdfWriter = PdfReader = None


def job_list(request):
    jobs = SQBJob.objects.all()
    q = request.GET.get("q")
    if q:
        jobs = jobs.filter(job_number__icontains=q)

    rows = []
    n_complete = n_partial = n_empty = 0
    total_types = len(SQB_DOCUMENT_TYPES)
    for job in jobs:
        uploaded, total = job.progress()
        if uploaded == total:
            n_complete += 1
        elif uploaded == 0:
            n_empty += 1
        else:
            n_partial += 1
        rows.append({"job": job, "uploaded": uploaded, "total": total})

    return render(request, "sqb/job_list.html", {
        "rows": rows, "n_complete": n_complete, "n_partial": n_partial,
        "n_empty": n_empty, "total_jobs": jobs.count(),
    })


@role_required("admin", "editor")
def job_create(request):
    if request.method == "POST":
        job_number = request.POST.get("job_number", "").strip()
        job_name = request.POST.get("job_name", "").strip()
        permit_number = request.POST.get("permit_number", "").strip()
        if not job_number:
            messages.error(request, "Job number is required.")
        elif SQBJob.objects.filter(job_number=job_number).exists():
            messages.error(request, "A job with this number already exists.")
        else:
            SQBJob.objects.create(job_number=job_number, job_name=job_name, permit_number=permit_number)
            messages.success(request, "Job created.")
            return redirect("sqb:list")
    return render(request, "sqb/job_form.html")


def job_detail(request, job_number):
    job = get_object_or_404(SQBJob, job_number=job_number)
    doc_map = {d.doc_type: d for d in job.documents.all()}
    checklist = [{"doc_type": dt, "doc": doc_map.get(dt)} for dt in SQB_DOCUMENT_TYPES]
    uploaded, total = job.progress()

    if request.method == "POST" and "save_permit" in request.POST:
        job.permit_number = request.POST.get("permit_number", "").strip()
        job.save()
        messages.success(request, "Permit number saved.")
        return redirect("sqb:detail", job_number=job.job_number)

    if request.method == "POST" and "delete_job" in request.POST:
        job.delete()
        messages.success(request, "Job deleted.")
        return redirect("sqb:list")

    return render(request, "sqb/job_detail.html", {
        "job": job, "checklist": checklist, "uploaded": uploaded, "total": total,
    })


@role_required("admin", "editor")
def upload_documents(request, job_number):
    job = get_object_or_404(SQBJob, job_number=job_number)
    if request.method == "POST":
        saved = 0
        for doc_type in SQB_DOCUMENT_TYPES:
            f = request.FILES.get(f"file_{doc_type}")
            if f:
                doc, _ = SQBDocument.objects.get_or_create(job=job, doc_type=doc_type)
                doc.file = f
                doc.uploaded_by = request.user
                doc.save()
                saved += 1
        if saved:
            messages.success(request, f"{saved} document(s) saved.")
        else:
            messages.warning(request, "No files were selected.")
    return redirect("sqb:detail", job_number=job.job_number)


@role_required("admin", "editor")
def compile_pdf(request, job_number):
    job = get_object_or_404(SQBJob, job_number=job_number)
    uploaded, total = job.progress()

    if PdfWriter is None:
        messages.error(request, "pypdf isn't installed on the server — add it to requirements.txt.")
        return redirect("sqb:detail", job_number=job.job_number)

    if uploaded < total:
        messages.error(request, "All documents must be uploaded before compiling.")
        return redirect("sqb:detail", job_number=job.job_number)

    doc_map = {d.doc_type: d for d in job.documents.all()}
    writer = PdfWriter()
    for doc_type in SQB_DOCUMENT_TYPES:
        doc = doc_map.get(doc_type)
        if doc and doc.file:
            try:
                doc.file.open("rb")
                reader = PdfReader(doc.file)
                for page in reader.pages:
                    writer.add_page(page)
            finally:
                doc.file.close()

    buffer = io.BytesIO()
    writer.write(buffer)
    response = HttpResponse(buffer.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="SQB_{job.job_number}_compiled.pdf"'
    return response
