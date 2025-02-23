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
    time = models.IntegerField(help_text="Time in seconds")
    points = models.IntegerField(default=1)
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name="questions")

    def __str__(self):
        return f"Question {self.id} - {self.evaluation.title}"

class Answer(models.Model):
    content = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer - {self.question.evaluation.title}"


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
    submission_date = models.DateTimeField(auto_now_add=True)
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
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name="student_answers")
    is_correct = models.BooleanField(blank=True)
    score = models.FloatField(default=0)

    def __str__(self):
        return f"Answer {self.id} - {self.submission.student.username} - {self.question.id}"