import json
import re


# 讀取 english_straegy.txt
file_path = "/Users/shiaupi/Desktop/my-llm-project/my_data/english_straegy.txt"
with open(file_path, "r", encoding="utf-8") as file:
    raw_text = file.read()

# 用標題符號 📌 🔹 來切割
sections = re.split(r"(📌|🔹)", raw_text)

# 整理成 JSON
data_chunks = []
temp_text = ""
chunk_size = 2  # 每 2 段合併成 1 個 Chunk，避免切得太細

for i in range(0, len(sections), chunk_size):
    temp_text = " ".join(sections[i:i+chunk_size]).strip()
    if len(temp_text) > 50:  # 避免太短的段落
        data_chunks.append({"source": "strategy", "content": temp_text})

with open("strategy_chunks.json", "w", encoding="utf-8") as file:
    json.dump(data_chunks, file, ensure_ascii=False, indent=4)

print("✅ `english_straegy.txt` 切割完成，已存為 strategy_chunks.json！")
