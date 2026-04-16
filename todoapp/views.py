import os
import json

from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin

import google.generativeai as genai

from .models import Task
from .forms import TaskForm


# ---------------------------------------------------------------------------
# Task CRUD Views (Class-Based)
# ---------------------------------------------------------------------------

class TaskListView(SuccessMessageMixin, ListView):
    """Displays the full task list and handles creating new tasks via POST."""

    model = Task
    template_name = "task_list.html"
    context_object_name = "tasks"
    ordering = ["-created_at"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TaskForm()
        return context

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return self.get(request, *args, **kwargs)


class TaskToggleView(View):
    """Handles toggling a task's completed state via POST."""

    def post(self, request, pk):
        task = Task.objects.get(pk=pk)
        # If a hidden field sends the OLD value, flip it; otherwise read the checkbox.
        task.completed = request.POST.get("completed") == "on"
        task.save()
        from django.shortcuts import redirect
        return redirect("task-list")


class TaskUpdateView(SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task_update.html"
    success_url = reverse_lazy("task-list")
    success_message = "Task updated successfully."


class TaskDeleteView(DeleteView):
    model = Task
    template_name = "task_delete.html"
    success_url = reverse_lazy("task-list")


# ---------------------------------------------------------------------------
# AI Suggest View — powered by Google Gemini Flash
# ---------------------------------------------------------------------------

class AISuggestView(View):
    """
    POST { "prompt": "..." }
    Returns { "suggestions": ["task 1", "task 2", ...] }

    Uses the Google Gemini API (gemini-1.5-flash).
    Set GEMINI_API_KEY in your environment or .env file.
    """

    def post(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body)
            user_prompt = body.get("prompt", "").strip()
        except (json.JSONDecodeError, AttributeError):
            return JsonResponse({"error": "Invalid JSON body."}, status=400)

        if not user_prompt:
            return JsonResponse({"error": "Prompt is required."}, status=400)

        api_key = getattr(settings, "GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
        if not api_key:
            return JsonResponse(
                {"error": "GEMINI_API_KEY is not configured. Please add it to your .env file."},
                status=500,
            )

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        system_prompt = (
            "You are a productivity assistant. "
            "Given the user's goal or topic, return a JSON array of 5 concise, "
            "actionable task titles they should add to their to-do list. "
            "Respond with ONLY a raw JSON array — no markdown, no explanation. "
            'Example: ["Task A", "Task B", "Task C", "Task D", "Task E"]'
        )

        try:
            response = model.generate_content(f"{system_prompt}\n\nUser goal: {user_prompt}")
            raw = response.text.strip()
            # Safely parse the returned JSON array
            suggestions = json.loads(raw)
            if not isinstance(suggestions, list):
                raise ValueError("Expected a JSON array.")
        except Exception as exc:
            return JsonResponse({"error": f"AI error: {str(exc)}"}, status=500)

        return JsonResponse({"suggestions": suggestions})