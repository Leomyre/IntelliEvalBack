from django.urls import path
from .views import get_evaluation, list_evaluations_by_teacher, create_evaluation

urlpatterns = [
    path("evaluations/<int:evaluation_id>/", get_evaluation, name="get_evaluation"),
    path("evaluations/teacher/", list_evaluations_by_teacher, name="list_teacher_evaluations"),
    path("evaluations/create/", create_evaluation, name="create_evaluation"),
]
