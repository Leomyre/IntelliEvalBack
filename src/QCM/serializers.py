from rest_framework import serializers
from .models import Evaluation, Question, Reponse

class EvaluationSerializer(serializers.ModelSerializer):
    professeur = serializers.StringRelatedField()  # Afficher le nom du professeur au lieu de l'ID

    class Meta:
        model = Evaluation
        fields = '__all__'  # Inclut tous les champs

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class ReponseSerializer(serializers.ModelSerializer):
    etudiant = serializers.StringRelatedField()  # Afficher le nom de l'étudiant au lieu de l'ID
    evaluation = serializers.StringRelatedField()  # Afficher le titre de l'évaluation

    class Meta:
        model = Reponse
        fields = '__all__'
