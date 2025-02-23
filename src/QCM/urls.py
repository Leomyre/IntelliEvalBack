from django.urls import path
from .views import get_evaluation, list_evaluations_by_teacher, create_evaluation

urlpatterns = [
    path("evaluations/get/<str:evaluation_code>/", get_evaluation, name="get_evaluation"),
    path("evaluations/teacher/", list_evaluations_by_teacher, name="list_teacher_evaluations"),
    path("evaluations/create/", create_evaluation, name="create_evaluation"),
]
