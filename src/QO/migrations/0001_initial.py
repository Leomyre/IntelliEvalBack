# Generated by Django 5.1.6 on 2025-02-23 07:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=255)),
                ('support_cours', models.TextField(blank=True, null=True)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('professeur', models.ForeignKey(limit_choices_to={'role': 'teacher'}, on_delete=django.db.models.deletion.CASCADE, related_name='evaluations_qo', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenu', models.TextField()),
                ('temps', models.IntegerField(help_text='Temps en secondes')),
                ('points', models.IntegerField(default=1)),
                ('evaluation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='QO.evaluation')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionOuverte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_caracteres', models.IntegerField()),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='question_ouverte', to='QO.question')),
            ],
        ),
        migrations.CreateModel(
            name='ReponseEtudiantOuverte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reponse_libre', models.TextField()),
                ('etudiant', models.ForeignKey(limit_choices_to={'role': 'student'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('evaluation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reponses_ouvertes', to='QO.evaluation')),
                ('question_ouverte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reponses_ouvertes', to='QO.questionouverte')),
            ],
        ),
    ]
