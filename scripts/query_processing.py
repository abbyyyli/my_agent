import re

def process_user_input(user_input):
    """ 清理用戶輸入，去除無關字元，確保查詢更精準 """
    user_input = user_input.strip()
    user_input = re.sub(r'\s+', ' ', user_input)  # 移除多餘空格
    return {"query": user_input}
