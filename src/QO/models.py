from django.db import models
from Accounts.models import User

class Evaluation(models.Model):
    titre = models.CharField(max_length=255)
    support_cours = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=10, unique=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    professeur = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': User.Role.TEACHER},
        related_name="evaluations_qo"  # Ajout d'un related_name unique
    )


    def __str__(self):
        return f"{self.titre} ({self.professeur.username})"

class Question(models.Model):
    contenu = models.TextField()
    temps = models.IntegerField(help_text="Temps en secondes")
    points = models.IntegerField(default=1)
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name="questions")

    def __str__(self):
        return f"Question {self.id} - {self.evaluation.titre}"

class QuestionOuverte(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='question_ouverte')
    max_caracteres = models.IntegerField()

    def __str__(self):
        return f"Question Ouverte {self.question.id} - {self.question.evaluation.titre}"

class ReponseEtudiantOuverte(models.Model):
    etudiant = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': User.Role.STUDENT})
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name="reponses_ouvertes")
    question_ouverte = models.ForeignKey(QuestionOuverte, on_delete=models.CASCADE, related_name='reponses_ouvertes')
    reponse_libre = models.TextField()

    def __str__(self):
        return f"Réponse Ouverte de {self.etudiant.username} - {self.evaluation.titre}"
