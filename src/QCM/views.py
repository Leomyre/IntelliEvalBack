from rest_framework import generics, permissions
from .models import Evaluation, Question, Reponse
from .serializers import EvaluationSerializer, QuestionSerializer, ReponseSerializer

# Evaluations
class EvaluationListCreateView(generics.ListCreateAPIView):
    queryset = Evaluation.objects.all().order_by('-date_creation')
    serializer_class = EvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]

class EvaluationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]

# Questions
class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

# Réponses
class ReponseListCreateView(generics.ListCreateAPIView):
    queryset = Reponse.objects.all()
    serializer_class = ReponseSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReponseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reponse.objects.all()
    serializer_class = ReponseSerializer
    permission_classes = [permissions.IsAuthenticated]
