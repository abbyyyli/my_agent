import json
import qdrant_client
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import numpy as np

# 連接 Qdrant
qdrant = qdrant_client.QdrantClient("http://localhost:6333")

# Collection 名稱
collection_name = "strategy_analysis"

# **檢查 Collection 是否存在**
collections = qdrant.get_collections()
existing_collections = [c.name for c in collections.collections]

if collection_name not in existing_collections:
    print(f"⚠️ `{collection_name}` 不存在，正在創建...")
    qdrant.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )
    print(f"✅ Collection `{collection_name}` 已創建！")
else:
    print(f"⚠️ Collection `{collection_name}` 已存在，跳過創建。")

# **讀取 `strategy_chunks.json`**
with open("strategy_chunks.json", "r", encoding="utf-8") as file:
    strategies = json.load(file)  # 確保 strategies 是 JSON 格式的列表

# **初始化 Embedding 模型**
embedding_model = "all-MiniLM-L6-v2"
model = SentenceTransformer(embedding_model)

# **轉換為向量，並存入 Qdrant**
for idx, strategy in enumerate(strategies):
    text = strategy["content"]
    embedding = model.encode(text).tolist()
    
    qdrant.upsert(
        collection_name=collection_name,
        points=[PointStruct(
            id=idx,
            vector=embedding,
            payload={"content": text}
        )]
    )

print(f"✅ `strategy_chunks.json` 已存入 Qdrant（共 {len(strategies)} 條）！")
