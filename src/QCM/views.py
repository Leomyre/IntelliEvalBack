from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status

from Accounts.models import User
from .models import Evaluation, Question, Answer
from .serializers import EvaluationSerializer
from QO.models import OpenQuestion

# Obtenir une évaluation spécifique avec ses questions et réponses
@api_view(["GET"])
#@permission_classes([IsAuthenticated])
def get_evaluation(request, evaluation_code):
    try:
        evaluation = Evaluation.objects.prefetch_related("questions").get(code=evaluation_code)
    except Evaluation.DoesNotExist:
        return Response({"error": "Évaluation non trouvée"}, status=status.HTTP_404_NOT_FOUND)

    # Construire la réponse JSON manuellement
    evaluation_data = {
        "title": evaluation.title,
        "course_material": evaluation.course_material,
        "creation_date": evaluation.creation_date,
        "teacher": {
            "id": evaluation.teacher.id,
            "username": evaluation.teacher.username,
        },
        "questions": []
    }

    # Récupérer toutes les questions liées à l'évaluation
    questions = evaluation.questions.all()
    
    for question in questions:
        question_data = {
            "id": question.id,
            "content": question.content,
            "time": question.time_limit,
            "type": "open" if hasattr(question, "question_ouverte") else "qcm"
        }

        # Vérifier si la question est une QuestionOuverte
        if hasattr(question, "question_ouverte"):
            question_data["max_characters"] = question.question_ouverte.max_caracteres
        else:
            # Si c'est un QCM, on ajoute les réponses (si elles existent)
            if hasattr(question, "answers"):
                question_data["answers"] = [
                    {
                        "id": answer.id,
                        "content": answer.content,
                        "is_correct": answer.is_correct
                    }
                    for answer in question.answers.all()
                ]
        
        evaluation_data["questions"].append(question_data)

    return Response({"evaluation": evaluation_data}, status=status.HTTP_200_OK)

# Obtenir toutes les évaluations créées par un professeur
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_evaluations_by_teacher(request):

    evaluations = Evaluation.objects.all()
    serializer = EvaluationSerializer(evaluations, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def create_evaluation(request):
   # Création d'une évaluation avec ses questions et réponses

    data = request.data.get("evaluation", {})

    # Vérifier que toutes les données nécessaires sont présentes
    required_fields = ["title", "course_material", "code", "questions"]
    for field in required_fields:
        if field not in data:
            return Response({f"error": f"Le champ {field} est requis."}, status=status.HTTP_400_BAD_REQUEST)

    # Créer l'évaluation
    evaluation = Evaluation.objects.create(
        title=data["title"],
        course_material=data["course_material"],
        code=data["code"],
        teacher=User.objects.get(id=3),
    )

    # Ajouter les questions
    for question_data in data["questions"]:
        if question_data["type"] == "qcm":
            question = Question.objects.create(
                evaluation=evaluation,
                content=question_data["content"],
                time=question_data["time"],
                points=question_data["points"]
            )
            # Ajouter les réponses associées
            for answer_data in question_data["answers"]:
                Answer.objects.create(
                    question=question,
                    content=answer_data["content"],
                    is_correct=answer_data["is_correct"]
                )
        
        elif question_data["type"] == "open":
            OpenQuestion.objects.create(
                evaluation=evaluation,
                content=question_data["content"],
                time_limit=question_data["time_limit"], 
            )

    return Response({"message": "Évaluation créée avec succès"}, status=status.HTTP_201_CREATED)
