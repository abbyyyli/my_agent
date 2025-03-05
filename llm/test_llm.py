import sys
from pathlib import Path

# 將專案根目錄添加到 PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

import unittest
from llm.llm_connect import LLMConnector

class TestLLMConnector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 初始化 LLMConnector 實例
        cls.llm_connector = LLMConnector(model="gpt-3.5-turbo", temperature=0.7)

    def test_generate_response_success(self):
        """
        測試 LLM 成功回應。
        """
        prompt = "What is the capital of France?"
        response = self.llm_connector.generate_response(prompt)

        print(f"Response: {response}")  # Debug 輸出
        self.assertIn("Paris", response)

    def test_generate_response_empty_input(self):
        """
        測試空輸入的回應是否合理。
        """
        invalid_prompt = ""  # 空輸入
        response = self.llm_connector.generate_response(invalid_prompt)

        print(f"Response for empty input: {response}")  # Debug 輸出
        self.assertIn("How can I assist you", response)

    def test_generate_response_invalid_key(self):
        """
        測試無效 API key 是否能正確處理錯誤。
        """
        # 使用無效的 API key 測試
        invalid_connector = LLMConnector(model="gpt-3.5-turbo", temperature=0.7)
        invalid_connector.client.openai_api_key = "invalid_key"

        try:
            response = invalid_connector.generate_response("Test")
        except Exception as e:
            print(f"Error with invalid API key: {e}")  # Debug 輸出
            self.assertIn("invalid API key", str(e).lower())

if __name__ == "__main__":
    unittest.main()
