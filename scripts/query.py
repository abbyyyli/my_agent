import json
import sys
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# **Qdrant 連接**
qdrant = QdrantClient("http://localhost:6333")

# **Collection 名稱**
collections = {
    "chat": "chat_history",
    "relationship": "relationship_analysis",
    "strategy": "strategy_analysis"
}

# **載入 Embedding 模型**
embedding_model = "all-MiniLM-L6-v2"
model = SentenceTransformer(embedding_model)

def search_qdrant(collection, query, top_k=5):
    """ 在 Qdrant 搜尋最相關的內容 """
    query_vector = model.encode(query).tolist()
    search_results = qdrant.search(
        collection_name=collection,
        query_vector=query_vector,
        limit=top_k
    )
    return [res.payload["content"] for res in search_results]

def filter_top_results(query, results, top_n=3):
    """ 根據語義相似度過濾最相關的回應 """
    query_vector = model.encode([query])
    result_vectors = [model.encode([r]) for r in results]
    
    similarities = [cosine_similarity(query_vector, vec)[0][0] for vec in result_vectors]
    
    # 依據相似度排序，取前 top_n 個結果
    sorted_results = [res for _, res in sorted(zip(similarities, results), reverse=True)]
    return sorted_results[:top_n]

# **用戶輸入查詢**
if len(sys.argv) > 1:
    query = " ".join(sys.argv[1:])
else:
    query = input("🔍 輸入你的感情問題: ")

# **查詢並篩選最相關的回應**
chat_results = filter_top_results(query, search_qdrant(collections["chat"], query))
relationship_results = filter_top_results(query, search_qdrant(collections["relationship"], query))
strategy_results = filter_top_results(query, search_qdrant(collections["strategy"], query))

# **輸出結果**
print("\n🔍 **相關聊天記錄**:")
for res in chat_results:
    print(f"💬 {res}\n")

print("\n📌 **感情分析建議**:")
for res in relationship_results:
    print(f"💡 {res}\n")

print("\n🧠 **心理學策略建議**:")
for res in strategy_results[:2]:  # 只取前 2 條策略
    print(f"📖 {res}\n")
