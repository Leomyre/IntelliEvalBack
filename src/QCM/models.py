from django.db import models
from Accounts.models import User

class Evaluation(models.Model):
    title = models.CharField(max_length=255)
    course_material = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=10, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': User.Role.TEACHER},
        related_name="evaluations_qcm"
    )

    def __str__(self):
        return f"{self.title} ({self.teacher.username})"

class Question(models.Model):
    content = models.TextField()
    correct_answer = models.TextField()
    time = models.IntegerField(help_text="Time in seconds")
    points = models.IntegerField(default=1)
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name="questions")

    def __str__(self):
        return f"Question {self.id} - {self.evaluation.title}"

class Answer(models.Model):
    content = models.TextField()
    score = models.FloatField(default=0)
    comment = models.TextField(blank=True, null=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': User.Role.STUDENT})
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")

    def __str__(self):
        return f"Answer by {self.student.username} - {self.evaluation.title}"


class Submission(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': User.Role.STUDENT},
        related_name="submissions"
    )
    evaluation = models.ForeignKey(
        Evaluation,
        on_delete=models.CASCADE,
        related_name="submissions"
    )
    date_soumission = models.DateTimeField(auto_now_add=True)
    score_total = models.FloatField(default=0)

    def __str__(self):
        return f"Submission {self.id} - {self.student.username} - {self.evaluation.title}"

class StudentAnswer(models.Model):
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        related_name="student_answers"
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="student_answers"
    )
    answer_text = models.TextField()
    is_correct = models.BooleanField(null=True, blank=True)
    score = models.FloatField(default=0)

    def __str__(self):
        return f"Answer {self.id} - {self.submission.student.username} - {self.question.id}"