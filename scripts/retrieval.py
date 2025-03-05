import requests
from sentence_transformers import SentenceTransformer
import os

# Qdrant 配置
QDRANT_URL = "http://localhost:6333"  # 本地運行 Qdrant

# Collection 名稱（將會使用不同的 Collection）
collections = {
    "chat": "chat_history",            # 用於聊天記錄的 Collection
    "relationship": "relationship_analysis",  # 用於感情分析的 Collection
    "strategy": "strategy_analysis"     # 用於策略分析的 Collection
}

# 初始化 SentenceTransformer 模型
embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(embedding_model)

def retrieve_top_k(query, collection, k=5):
    """
    從指定的 Qdrant Collection 檢索最相關的文本
    :param query: 用戶的查詢問題
    :param collection: Qdrant 中的 Collection 名稱
    :param k: 返回最相關結果的數量
    :return: 最相關的文本結果
    """
    # 轉換查詢為向量
    query_vector = model.encode([query])[0].tolist()

    # 檢查向量維度（應為 384）
    if len(query_vector) != 384:
        raise ValueError(f"❌ 查詢向量維度錯誤：應為 384，實際為 {len(query_vector)}")

    # 構建查詢負載
    search_payload = {
        "vector": query_vector,  # 查詢向量
        "top": k,                 # 返回前 k 條結果
        "with_payload": True      # 返回與點相關的 payload（文本內容）
    }

    # 發送查詢請求
    response = requests.post(f"{QDRANT_URL}/collections/{collection}/points/search", json=search_payload)

    # 檢查 API 請求狀態
    if response.status_code != 200:
        print(f"❌ 請求錯誤：{response.json()}")
        return []

    response_json = response.json()

    # 檢查返回結果是否包含 `result` 字段
    if "result" not in response_json:
        print(f"❌ 回應無結果：{response_json}")
        return []

    results = response_json["result"]

    # 如果沒找到結果
    if not results:
        print("⚠️ 沒有找到相關數據！")
        return []

    # 根據 `payload` 返回對應的文本（檢查是否包含 `text` 字段）
    result_texts = []
    for res in results:
        # 檢查是否有 "text" 或 "content" 字段，若有則提取
        if "text" in res["payload"]:
            result_texts.append(res["payload"]["text"])
        elif "content" in res["payload"]:
            result_texts.append(res["payload"]["content"])  # 如果沒有 `text`，用 `content`
        else:
            result_texts.append("無法提取內容")

    return result_texts
