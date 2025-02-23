from django.db import models
from Accounts.models import User
from QCM.models import Evaluation, Submission

class OpenQuestion(models.Model):
    content = models.TextField()
    time_limit = models.IntegerField(help_text="Time in seconds", default=60)
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name="questions")

    def __str__(self):
        return f"Question {self.id} - {self.evaluation.title}"


class OpenStudentResponse(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='open_responses')
    open_question = models.ForeignKey(OpenQuestion, on_delete=models.CASCADE, related_name='open_responses')
    response_text = models.TextField()
    points = models.IntegerField(default=1)
    
    def __str__(self):
        return f"Response by {self.submission.student.username} - {self.open_question.question.evaluation.title}"
