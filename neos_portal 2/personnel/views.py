from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from .forms import PersonnelForm
from .models import Personnel


def personnel_list(request):
    people = Personnel.objects.all()
    q = request.GET.get("q")
    if q:
        people = people.filter(full_name__icontains=q)
    return render(request, "personnel/personnel_list.html", {"people": people, "total": people.count()})


@role_required("admin", "editor")
def personnel_create(request):
    if request.method == "POST":
        form = PersonnelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Added.")
            return redirect("personnel:list")
    else:
        form = PersonnelForm()
    return render(request, "personnel/personnel_form.html", {"form": form, "mode": "add"})


@role_required("admin", "editor")
def personnel_edit(request, person_id):
    person = get_object_or_404(Personnel, id=person_id)
    if request.method == "POST":
        form = PersonnelForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            messages.success(request, "Saved.")
            return redirect("personnel:list")
    else:
        form = PersonnelForm(instance=person)
    return render(request, "personnel/personnel_form.html", {"form": form, "person": person, "mode": "edit"})


@role_required("admin", "editor")
def personnel_delete(request, person_id):
    person = get_object_or_404(Personnel, id=person_id)
    if request.method == "POST":
        person.delete()
        messages.success(request, "Deleted.")
        return redirect("personnel:list")
    return render(request, "personnel/personnel_confirm_delete.html", {"person": person})
