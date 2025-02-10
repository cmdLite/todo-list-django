import logging
from typing import Optional
from django.shortcuts import redirect, render
from .models import Task
from .forms import TaskForm

logger = logging.getLogger('debug')

# Create your views here.
def task_list(request, pk: Optional[int] = None):
    tasks = Task.objects.all()

    if 'completed' in request.POST:
            taskpatch = Task.objects.get(id=pk)
            taskpatch.completed = request.POST.get('completed') == 'on'
            taskpatch.save()
            return redirect("task-list")
    else:
            form = TaskForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("task-list")

    context = {"tasks":tasks, "form":form}
    return render(request, "task_list.html", context)

def task_patch(request,pk):
    taskpatch = Task.objects.get(id=pk)



    context = {"taskpatch":taskpatch}
    return render(request, "task_list.html", context)

def task_update(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task-list")
        
    context = {"form": form}
    return render(request, "task_list.html", context)

def task_delete(request, pk):
    task = Task.objects.get(id=pk)

    if request.method == "POST":
        task.delete()
        return redirect("task-list")
    
    context={"task":task}
    return render(request, "task_delete.html", context)