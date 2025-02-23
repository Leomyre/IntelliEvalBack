from rest_framework import serializers
from .models import OpenQuestion, OpenStudentResponse
from QCM.models import Submission

class OpenQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenQuestion
        fields = '__all__'

class OpenStudentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenStudentResponse
        fields = '__all__'
