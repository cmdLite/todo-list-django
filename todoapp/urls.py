from django.urls import path
from .views import (
    TaskListView,
    TaskUpdateView,
    TaskDeleteView,
    TaskToggleView,
    AISuggestView,
)

urlpatterns = [
    path("", TaskListView.as_view(), name='task-list'),
    path("toggle/<int:pk>/", TaskToggleView.as_view(), name='task-toggle'),
    path("update/<int:pk>/", TaskUpdateView.as_view(), name='task-update'),
    path("delete/<int:pk>/", TaskDeleteView.as_view(), name='task-delete'),
    path("api/ai/suggest/", AISuggestView.as_view(), name='ai-suggest'),
]