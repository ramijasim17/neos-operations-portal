from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ActionItemForm
from .models import ActionItem, ActionStep, Status


def action_list(request):
    actions = ActionItem.objects.exclude(status=Status.COMPLETED)
    completed = ActionItem.objects.filter(status=Status.COMPLETED)

    counts = {
        "high": actions.filter(priority="High").count(),
        "progress": actions.filter(status=Status.IN_PROGRESS).count(),
        "completed": completed.count(),
        "total": actions.count(),
    }
    return render(request, "action_tracker/action_list.html", {
        "actions": actions, "completed": completed, "counts": counts,
    })


def action_create(request):
    if request.method == "POST":
        form = ActionItemForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.status = Status.PENDING
            obj.created_by = request.user
            obj.save()
            for line in form.cleaned_data.get("steps_text", "").split("\n"):
                line = line.strip()
                if line:
                    ActionStep.objects.create(action=obj, step_description=line)
            messages.success(request, "Action created.")
            return redirect("action_tracker:list")
    else:
        form = ActionItemForm()
    return render(request, "action_tracker/action_form.html", {"form": form})


def action_detail(request, action_id):
    action = get_object_or_404(ActionItem, id=action_id)

    if request.method == "POST":
        if "add_step" in request.POST:
            desc = request.POST.get("new_step", "").strip()
            if desc:
                ActionStep.objects.create(action=action, step_description=desc)
        elif "toggle_step" in request.POST:
            step = get_object_or_404(ActionStep, id=request.POST["toggle_step"])
            step.is_completed = not step.is_completed
            step.save()
            done, total = action.progress
            if total:
                action.status = (
                    Status.COMPLETED if done == total
                    else Status.PENDING if done == 0
                    else Status.IN_PROGRESS
                )
                action.save()
        elif "save_status" in request.POST:
            action.status = request.POST.get("status", action.status)
            action.save()
        elif "save_comments" in request.POST:
            action.comments = request.POST.get("comments", "")
            action.save()
            messages.success(request, "Notes saved.")
        elif "delete" in request.POST:
            action.delete()
            messages.success(request, "Deleted.")
            return redirect("action_tracker:list")
        return redirect("action_tracker:detail", action_id=action.id)

    return render(request, "action_tracker/action_detail.html", {
        "action": action, "steps": action.steps.all(), "statuses": Status.choices,
    })
