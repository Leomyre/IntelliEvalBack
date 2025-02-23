from django.db import models
from Accounts.models import User

class Evaluation(models.Model):
    title = models.CharField(max_length=255)
    course_support = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=10, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    teacher = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': User.Role.TEACHER},
        related_name="evaluations_qo"
    )

    def __str__(self):
        return f"{self.title} ({self.teacher.username})"

class Question(models.Model):
    content = models.TextField()
    time = models.IntegerField(help_text="Time in seconds")
    points = models.IntegerField(default=1)
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name="questions")

    def __str__(self):
        return f"Question {self.id} - {self.evaluation.title}"

class OpenQuestion(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='open_question')
    max_characters = models.IntegerField()

    def __str__(self):
        return f"Open Question {self.question.id} - {self.question.evaluation.title}"

class StudentOpenResponse(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': User.Role.STUDENT})
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name="open_responses")
    open_question = models.ForeignKey(OpenQuestion, on_delete=models.CASCADE, related_name='open_responses')
    free_response = models.TextField()

    def __str__(self):
        return f"Open Response from {self.student.username} - {self.evaluation.title}"