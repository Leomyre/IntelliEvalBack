from django.urls import path
from .views import EvaluationListCreateView, EvaluationDetailView, QuestionListCreateView, QuestionDetailView, ReponseListCreateView, ReponseDetailView

urlpatterns = [
    # Routes pour les Evaluations
    path('api/evaluations/', EvaluationListCreateView.as_view(), name='evaluation-list-create'),
    path('api/evaluations/<int:pk>/', EvaluationDetailView.as_view(), name='evaluation-detail'),

    # Routes pour les Questions
    path('api/questions/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('api/questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),

    # Routes pour les Réponses
    path('api/reponses/', ReponseListCreateView.as_view(), name='reponse-list-create'),
    path('api/reponses/<int:pk>/', ReponseDetailView.as_view(), name='reponse-detail'),
]
