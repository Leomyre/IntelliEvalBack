from django.db import models
from Accounts.models import User

class Evaluation(models.Model):
    title = models.CharField(max_length=255)
    course_material = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': User.Role.TEACHER})

    def __str__(self):
        return f"{self.title} ({self.teacher.username})"

class Question(models.Model):
    content = models.TextField()
    time_limit = models.IntegerField(help_text="Time in seconds", default=60)
    points = models.IntegerField(default=1)
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name="questions")


    def __str__(self):
        return f"Question {self.id} - {self.evaluation.title}"

class OpenQuestion(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='open_question')
    max_characters = models.IntegerField()

    def __str__(self):
        return f"Open Question {self.question.id} - {self.question.evaluation.title}"

class Submission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': User.Role.STUDENT})
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    total_score = models.FloatField()

    def __str__(self):
        return f"Submission by {self.student.username} - {self.evaluation.title}"

class OpenStudentResponse(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='open_responses')
    open_question = models.ForeignKey(OpenQuestion, on_delete=models.CASCADE, related_name='open_responses')
    response_text = models.TextField()

    def __str__(self):
        return f"Response by {self.submission.student.username} - {self.open_question.question.evaluation.title}"
