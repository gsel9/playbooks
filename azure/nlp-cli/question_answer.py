"""
See tutorial Develop natural language solutions in Azure - Create 
question answering solutions with Azure Language for how to deploy
a Q&A service.
"""

from dotenv import load_dotenv
import os

from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient


def main():
    try:
        # Get Configuration Settings
        load_dotenv()
        endpoint = os.getenv('LANGUAGE_ENDPOINT')
        key = os.getenv('LANGUAGE_KEY')
        project_name = os.getenv('QA_PROJECT_NAME')
        deployment_name = os.getenv('QA_DEPLOYMENT_NAME')

        # Create client using endpoint and key
        credential = AzureKeyCredential(key)
        client = QuestionAnsweringClient(endpoint=endpoint, credential=credential)

        # Submit a question and display the answer
        user_question = ""
        while True:
            user_question = input("Question: ")
            if user_question.lower() == "quit":
                print("Goodbye!")
                break 
            response = client.get_answers(
                question=user_question,
                project_name=project_name,
                deployment_name=deployment_name
            )
            for candicate in response.answers:
                print(candicate.answer)
                print(f"Confidence: {candicate.confidence}")
                print(f"Source: {candicate.source}")

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
