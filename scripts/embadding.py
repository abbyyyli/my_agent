import json
import qdrant_client
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import numpy as np

qdrant = qdrant_client.QdrantClient("http://localhost:6333")

# 確保 Qdrant 伺服器已經在執行
try:
    qdrant.get_collections()
    print("✅ 成功連接到 Qdrant 伺服器！")
except Exception as e:
    print(f"❌ 無法連接 Qdrant 伺服器，請確認是否運行中: {e}")
    exit()
    
# 創建 Collection（如果尚未建立）
collection_name = "chat_history"
qdrant.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

# 讀取聊天記錄
with open("chat_cleaned.json", "r", encoding="utf-8") as file:
    chat_chunks = json.load(file)

# 初始化 Embedding 模型
embedding_model = "all-MiniLM-L6-v2"
model = SentenceTransformer(embedding_model)

# 轉換對話為向量，並存入 Qdrant
documents = []
for idx, chunk in enumerate(chat_chunks):
    text = chunk["content"]
    embedding = model.encode(text).tolist()
    
    # 存入 Qdrant
    qdrant.upsert(
        collection_name=collection_name,
        points=[PointStruct(
            id=idx,
            vector=embedding,
            payload={"timestamp": chunk["timestamp"], "content": text}
        )]
    )

print(f"✅ 聊天記錄已存入 Qdrant（共 {len(chat_chunks)} 條）！")
