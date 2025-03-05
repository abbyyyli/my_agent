import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

class LLMConnector:
    def __init__(self, model="gpt-3.5-turbo", temperature=0.7):
        """
        初始化 LLM 客戶端
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set in environment variables!")

        self.client = ChatOpenAI(
            model=model,
            temperature=temperature,
            openai_api_key=api_key
        )

    def generate_response(self, prompt) -> str:
        """
        发送 Prompt 到 LLM 并获取结果
        """
        try:
            # 判断输入是否为结构化数据
            if isinstance(prompt, dict) and "messages" in prompt:
                messages = prompt["messages"]
                # 修改调用方式，确保符合 invoke 方法的要求
                response = self.client.invoke(input=messages)
            elif isinstance(prompt, str):
                response = self.client.invoke(input=prompt)
            else:
                raise ValueError("Invalid input format for prompt.")
            return response.content
        except Exception as e:
            return f"Error querying LLM: {str(e)}"
