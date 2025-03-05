from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from scripts.prompt_template import create_prompt  # ✅ 這樣只導入函數，不會造成循環

load_dotenv()

class LLMConnector:
    def __init__(self, model="gpt-3.5-turbo", temperature=0.7):
        """
        Initialize the LLM client
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set in environment variables!")

        self.client = ChatOpenAI(
            model=model,
            temperature=temperature,
            openai_api_key=api_key
        )

    def generate_response(self, query, retrieved_texts) -> str:
        """
        Generate response using LLM and structured prompt
        """
        try:
            prompt = create_prompt(query, retrieved_texts)
            response = self.client.invoke(input=prompt)
            return response.content
        except Exception as e:
            return f"Error querying LLM: {str(e)}"
