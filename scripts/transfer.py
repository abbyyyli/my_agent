import json
import re

# 讀取 .txt 聊天記錄
file_path = "/Users/shiaupi/Desktop/my-llm-project/my_data/[LINE] Chat with MAKKINS.txt"
with open(file_path, "r", encoding="utf-8") as file:
    raw_text = file.readlines()

# 解析 LINE 聊天格式
def parse_chat(lines):
    chat_data = []
    pattern = r"(\d{2}:\d{2})\t(.+?)\t(.+)"  # 解析時間、說話者、訊息
    current_date = None
    
    for line in lines:
        if re.match(r"[A-Za-z]{3}, \d{2}/\d{2}/\d{4}", line):  # 確認是日期行
            current_date = line.strip()
            continue

        match = re.match(pattern, line)
        if match and current_date:
            time = match.group(1)
            speaker = match.group(2)
            message = match.group(3)

            if "[Sticker]" not in message and "☎ Missed call" not in message and "[Photo]" not in message:
                chat_data.append({
                    "date": current_date,
                    "time": time,
                    "speaker": speaker,
                    "message": message
                })

    return chat_data

chat_data = parse_chat(raw_text)

# 進一步切割為「對話片段」
def chunk_conversations(conversations, chunk_size=5):
    chunks = []
    for i in range(0, len(conversations), chunk_size):
        chunk = conversations[i:i+chunk_size]
        text = "\n".join([f"{c['speaker']}: {c['message']}" for c in chunk])
        chunks.append({
            "timestamp": chunk[0]['date'] + " " + chunk[0]['time'],
            "content": text
        })
    return chunks

chat_chunks = chunk_conversations(chat_data)

# 儲存清理後的聊天記錄為 JSON
with open("chat_cleaned.json", "w", encoding="utf-8") as file:
    json.dump(chat_chunks, file, ensure_ascii=False, indent=4)

print("✅ 聊天記錄清理完成，已存為 chat_cleaned.json！")
