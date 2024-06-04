from langchain_community.embeddings import OllamaEmbeddings
import os
from pinecone import Pinecone
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
import google.generativeai as genai
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
embeddings = OllamaEmbeddings(model="llama3")
index_name="rag-movie-recomm"

pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)


def format_docs(docs):
    formatted_docs = []
    for doc in docs:
        metadata = doc.metadata
        formatted_doc = {
            "Title": metadata.get('Title', 'N/A'),
            "Plot": metadata.get('Plot', 'N/A'),
            "Genre": metadata.get('Genre', 'N/A'),
            "Runtime": metadata.get('Runtime', 'N/A'),
            "Release Year": metadata.get('Year', 'N/A'),
            "Actor": ', '.join(metadata.get('Actors', [])),
            "Director": metadata.get('Director', 'N/A'),
            "Website": metadata.get('Website', 'N/A'),
            "Poster": metadata.get('Poster', 'N/A'),
            "IMDB Rating": metadata.get('imdbRating', 'N/A'),
            "imdbID": metadata.get('imdbID', 'N/A'),
            "Reasoning": ""
        }
        formatted_docs.append(formatted_doc)
    return formatted_docs


class GeneralQuestionAnswering:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Configure the Gemini model with the API key
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        # self.model = genai.model("gemini-pro")
        self.model = ChatGoogleGenerativeAI(model="gemini-pro")

    def ask_question(self, question, context):
        # Define the prompt template
        prompt_template = """
            Recommend films based on the user's query and the provided context only. 
            Only recommend films if they are in the context and relevant.  
            Provide three to five relevant film recommendations, ensuring from the context only. 
            If the context is empty or none of the films are relevant, dont give anything you can return empty json response.
            Do not recommend more than five films.
            Don't give answer on based of your knowledge, you are strictly to use context provided for recommending the movies only.
            
            your response should be in json format only strictly.
            
            Use Context provided to give output of recommended movies in the below mentioned format for every movie, In the reasoning field in the output format, write your reason for recommending the movie make it as you are explaining why its a must watch movie:-
            
            OUTPUT FORMAT:
            [
                "Title": "",
                "Plot": "",
                "Genre":""
                "Runtime": "",
                "Release Year": "",
                "Actor": "",
                "Director": "",
                "Website": "",
                "Poster": "",
                "IMDB Rating": "",
                "imdbID": "",
                "Reasoning": ""
            ]
            
            Question: {question}
            Context: {context}
            """
        
        doc1  = format_docs(context)
        # print(doc1)
        prompt = prompt_template.format(question=question, context = doc1)
        # print(prompt)

        # Generate a response using the Gemini model
        response = self.model.invoke(prompt)
        # print(response)

        return response.content


# if __name__ == "__main__":
#     qa = GeneralQuestionAnswering()
#     question = input("Enter your question: ")
#     docsearch = PineconeVectorStore.from_existing_index(index_name, embeddings)
#     docs = docsearch.similarity_search(question)
#     answer = qa.ask_question(question, docs)
#     print("Answer:", answer)