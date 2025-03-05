from dotenv import load_dotenv
from scripts.query_processing import process_user_input
from scripts.retrieval import retrieve_top_k
from llm.llm_connect import LLMConnector
from scripts.prompt_template import create_prompt
import sys
import os

# **載入環境變數**
load_dotenv()

# **初始化 LLMConnector**
llm = LLMConnector(model="gpt-4", temperature=0.7)

# **獲取用戶輸入**
user_input = input("請輸入你的感情問題：")
processed_input = process_user_input(user_input)

# **執行 RAG 檢索**
chat_history = retrieve_top_k(processed_input["query"], "chat_history")
relationship_analysis = retrieve_top_k(processed_input["query"], "relationship_analysis")
strategy_analysis = retrieve_top_k(processed_input["query"], "strategy_analysis")

# **打印檢索結果**
print("\n🔍 **檢索到的內容**:")
print(f"\n📜 **Chat History (對話記錄)**: {chat_history}")
print(f"\n📖 **Relationship Analysis (關係分析)**: {relationship_analysis}")
print(f"\n🧠 **Strategy Analysis (策略分析)**: {strategy_analysis}")

# **檢查 Qdrant 是否返回結果**
if not chat_history and not relationship_analysis and not strategy_analysis:
    print("⚠️ Qdrant 未找到相關資料，請確認數據是否正確存入。")
    exit()

# **組合 Prompt**
final_prompt = create_prompt(
    processed_input["query"], chat_history, relationship_analysis, strategy_analysis
)

# **打印傳遞給 Prompt Template 的內容**
print("\n📝 **傳遞給 `create_prompt` 的內容**:")
print(final_prompt)

# **詢問 GPT-4**
response = llm.generate_response(final_prompt)

# **打印 AI 生成的回應**
print("\n🤖 **AI 生成的回應**:")
print(response)
