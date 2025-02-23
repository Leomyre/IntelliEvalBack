import time


from Accounts.models import *
from assistant import DatabaseAssistant
from helpers import get_model_structure
from django.apps import apps
from django.conf import settings
from django.db.models import Field
from django.http import JsonResponse

from openai import OpenAI
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


api_key = settings.OPENAI_API_KEY
# assistant = DatabaseAssistant()


table_structure = get_model_structure()


def generate_django_query_with_gpt3(question, table_structure):
    client = OpenAI(api_key=api_key)

    prompt = (
        f"Voici la structure simplifiée des modèles Django pour la base de données : {table_structure}\n\n"
        f"Question : {question}\n\n"
        f"Répondez avec l'expression Django QuerySet appropriée pour obtenir les résultats souhaités. "
        f"Ne fournissez aucune explication, juste le code du QuerySet. "
        f"Assurez-vous que la requête est valide et utilise correctement les champs et relations des modèles Django."
    )

    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=250,
        temperature=0.7,
    )

    django_query = response.choices[0].text
    print(django_query)
    return django_query


try:
    client = OpenAI(api_key=api_key)
    th = client.beta.threads.create()
except:
    client = None
    th = None


def generate_django_query_assistant(question, table_structure, thread):

    # Prepare the prompt with table structure and question
    prompt = f"""    
    Question: {question}
       Respond with the appropriate Django QuerySet expression to obtain the desired results. Do not provide any explanation, just the QuerySet code.
    Ensure that the query is valid and correctly uses the fields and relationships from the Django models.
    """

    try:
        client = OpenAI(api_key=api_key)
        if settings.N_RUN == 0:

            settings.N_RUN += 1

            contenue = f"""Voici la structure simplifiée des modèles Django pour la base de données : {table_structure}"""

            client.beta.threads.messages.create(
                thread_id=thread.id,
                role="assistant",
                content=contenue,
            )

        client.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=prompt
        )

        # Run the assistant with the provided prompt
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id="asst_McczzwmE7mve0zwkKwLeOUzu",
            model="gpt-3.5-turbo",
            temperature=0.7,
        )

        # Poll for the status of the run
        run_status = run.status
        while run_status in ["queued", "running"]:
            time.sleep(2)
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            run_status = run.status

        # Check if the run completed successfully
        if run_status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            assistant_response = None
            for msg in messages:
                if msg.role == "assistant":
                    assistant_response = msg.content[0].text.value
                    break

            if assistant_response:
                return assistant_response
            else:
                return Response(
                    {"error": "No response from the assistant"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return Response(
                {"error": "The run did not complete successfully"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def execute_and_display_query(django_query):
    try:
        if not isinstance(django_query, str):
            raise ValueError(
                "La requête générée n'est pas une chaîne de caractères valide."
            )

        query_result = eval(django_query)

        if hasattr(query_result, "values"):
            results = list(query_result.values())
        elif hasattr(query_result, "__dict__"):
            results = [query_result.__dict__]
        else:
            raise ValueError(
                "La requête générée ne renvoie pas un objet QuerySet ou un modèle valide."
            )

        results = [
            {k: v for k, v in result.items() if k != "_state"} for result in results
        ]

        return results

    except Exception as e:
        print(f"Error executing Django query: {e}")
        return {"error": str(e)}


def get_user_request(message):
    try:
        # sql_query = generate_django_query_with_gpt3(message, table_structure)
        sql_query = generate_django_query_assistant(message, table_structure, th)
        result = execute_and_display_query(sql_query)
        if isinstance(result, dict) and "error" in result:
            return result
        return result
    except Exception as e:
        return {"error": str(e)}


# def get_user_request(message):
#     try:
#         result = execute_and_display_query(sql_query)
#         if isinstance(result, dict) and "error" in result:
#             return result
#         return result
#     except Exception as e:
#         return {"error": str(e)}


def get_data_by_request(question):
    result = get_user_request(question)
    return result


@api_view(["POST"])
@permission_classes([AllowAny])
def test_database(request):
    question = "quel est la chambre d'une hébergement le plus chère de votre site?"
    response = get_data_by_request(question)
    return Response({"response": response})


{"message": "quel est la chambre d'une hébergement le plus chère de votre site?"}


def generate_sql_query_with_gpt3(question, table_structure):
    client = OpenAI(api_key=api_key)
    prompt = (
        f"Voici la structure des tables de la base de données: {table_structure}\n"
        f"Question: {question}\n"
        f"Répondez avec la requête SQL appropriée pour obtenir les résultats souhaités."
    )

    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=120,
        temperature=0.5,
    )

    sql_query = response.choices[0].text
    return sql_query

def generate_qcm(prompt):
        client = OpenAI(api_key=api_key)
        full_prompt = (
            f"Voici un prompt pour générer un QCM : {prompt}\n\n"
            f"Créez un questionnaire à choix multiples (QCM) basé sur ce prompt. "
            f"Assurez-vous d'inclure plusieurs questions avec des choix de réponses, et indiquez la réponse correcte pour chaque question."
        )

        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=full_prompt,
            max_tokens=500,
            temperature=0.7,
        )

        qcm = response.choices[0].text
        return qcm