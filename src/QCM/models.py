from django.db import models
from Accounts.models import User

class Evaluation(models.Model):
    titre = models.CharField(max_length=255)
    support_cours = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=10, unique=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    professeur = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': User.Role.TEACHER})

    def __str__(self):
        return f"{self.titre} ({self.professeur.username})"

class Question(models.Model):
    contenu = models.TextField()
    reponse_correcte = models.TextField()
    temps = models.IntegerField(help_text="Temps en secondes")
    points = models.IntegerField(default=1)
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name="questions")

    def __str__(self):
        return f"Question {self.id} - {self.evaluation.titre}"

class Reponse(models.Model):
    contenu = models.TextField()
    score = models.FloatField(default=0)
    commentaire = models.TextField(blank=True, null=True)
    etudiant = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': User.Role.STUDENT})
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name="reponses")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="reponses")

    def __str__(self):
        return f"Réponse de {self.etudiant.username} - {self.evaluation.titre}"
