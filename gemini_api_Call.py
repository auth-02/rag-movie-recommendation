import google.generativeai as genai
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI

class GeneralQuestionAnswering:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Configure the Gemini model with the API key
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        # self.model = genai.model("gemini-pro")
        self.model = ChatGoogleGenerativeAI(model="gemini-pro")

    def ask_question(self, question):
        # Define the prompt template
        prompt_template = """
            You are an expert in answering questions.
            You are tasked to provide a detailed and accurate answer to the given question:

            NOTE: Use only the information you have to provide the answer.

            Provide the output response in plain text.

            I will tip you $1000 if the user finds the answer helpful.

            <question>
            {user_question}
            </question>
        """
        
        # Format the prompt with the user's question
        prompt = prompt_template.format(user_question=question)

        # Generate a response using the Gemini model
        response = self.model.invoke(prompt)
        # print(response)

        return response.content

if __name__ == "__main__":
    qa = GeneralQuestionAnswering()
    question = input("Enter your question: ")
    answer = qa.ask_question(question)
    print("Answer:", answer)
