import os
import csv
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
import spacy

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
base_url = os.getenv("DEEPSEEK_BASE_URL")
model_name = os.getenv("DEEPSEEK_MODEL")

nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

llm = ChatOpenAI(
    api_key=api_key,
    base_url=base_url,
    model=model_name,
    temperature=0
)

@tool
def extract_words(file_path: str) -> str:
    """
    读取六级真题txt，spacy词形还原，过滤停用词，统计词频，导出csv
    Args:
        file_path: txt文件路径，例如 cet6_5year/2025.txt
    """
    if not os.path.exists(file_path):
        return f"❌ 文件不存在：{file_path}"
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    doc = nlp(text)
    word_freq = {}
    for token in doc:
        if token.is_alpha and not token.is_stop and len(token.text)>=2:
            lemma = token.lemma_.lower()
            word_freq[lemma] = word_freq.get(lemma, 0) + 1
    out_dir = "output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "word_freq.csv")
    sorted_items = sorted(word_freq.items(), key=lambda x:x[1], reverse=True)
    with open(out_path, "w", newline="", encoding="utf-8-sig") as cf:
        w = csv.writer(cf)
        w.writerow(["word", "count"])
        for word, cnt in sorted_items:
            w.writerow([word, cnt])
    return f"✅ 提取完成！共{len(word_freq)}个单词，结果保存到 {out_path}"

tools = [extract_words]
agent = create_react_agent(llm, tools)

print("==== 六级单词提取Agent｜DeepSeek版 ====")
print("示例指令：提取 cet6_5year/test.txt 的单词")
while True:
    user_msg = input("\n你：")
    if user_msg.lower() in ["q", "quit", "exit"]:
        break
    res = agent.invoke({"messages": [("user", user_msg)]})
    print("\nAgent：", res["messages"][-1].content)

