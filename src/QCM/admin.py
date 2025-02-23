from django.contrib import admin
from .models import Evaluation, Question, Answer, Submission, StudentAnswer

class AnswerInline(admin.TabularInline):  
    model = Answer  
    extra = 3  # Ajoute 3 champs de réponse par défaut  

class QuestionAdmin(admin.ModelAdmin):  
    list_display = ("id", "content", "evaluation", "time", "points")  
    list_filter = ("evaluation",)  
    search_fields = ("content",)  
    inlines = [AnswerInline]  

class EvaluationAdmin(admin.ModelAdmin):  
    list_display = ("id", "title", "code", "teacher", "creation_date")  
    list_filter = ("teacher", "creation_date")  
    search_fields = ("title", "code")  

class SubmissionAdmin(admin.ModelAdmin):  
    list_display = ("id", "student", "evaluation", "submission_date", "score_total")  
    list_filter = ("evaluation", "student")  
    search_fields = ("student__username", "evaluation__title")  

class StudentAnswerAdmin(admin.ModelAdmin):  
    list_display = ("id", "submission", "question", "answer", "is_correct", "score")  
    list_filter = ("submission__evaluation",)  
    search_fields = ("submission__student__username", "question__content")  

# Enregistrer les modèles dans l'admin
admin.site.register(Evaluation, EvaluationAdmin)  
admin.site.register(Question, QuestionAdmin)  
admin.site.register(Submission, SubmissionAdmin)  
admin.site.register(StudentAnswer, StudentAnswerAdmin)  
