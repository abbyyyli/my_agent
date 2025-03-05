import json
import re

# 讀取 conculsion.txt
file_path = "/Users/shiaupi/Desktop/my-llm-project/my_data/conculsion.txt"
with open(file_path, "r", encoding="utf-8") as file:
    raw_text = file.read()

# 使用換行 / 事件標題來切割
sections = re.split(r"\n{2,}", raw_text)  # 依照兩個換行符號作為分段

# 儲存為 JSON
data_chunks = []
for section in sections:
    section = section.strip()
    if len(section) > 50:  # 避免太短的段落
        data_chunks.append({"source": "conculsion", "content": section})

with open("conculsion_chunks.json", "w", encoding="utf-8") as file:
    json.dump(data_chunks, file, ensure_ascii=False, indent=4)

print("✅ `conculsion.txt` 切割完成，已存為 conculsion_chunks.json！")
