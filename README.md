CET-6 单词提取 Agent 项目说明文档
本项目是一个基于 LangChain + LangGraph 的智能 Agent，专为英语六级（CET-6）备考设计。它能够自动读取历年真题文本文件，通过自然语言处理技术提取高频核心词汇，并导出为 CSV 表格，帮助你高效整理复习重点。
一、项目简介
本 Agent 由 DeepSeek 大模型驱动，支持自然语言指令交互，核心功能如下：
•  自动读取真题文本：支持批量处理 cet6_5year/ 目录下的 .txt 格式真题文件。
•  智能词汇提取：结合 spaCy 进行词形还原（Lemmatization），去除停用词（Stopwords），并统计词频。
•  CSV 结果导出：将提取的高频词汇以结构化表格形式保存，方便导入 Excel 或 Anki 等工具复习。
•  交互式 Agent：基于 DeepSeek 大模型驱动，支持自然语言指令交互（如“提取 cet6_5year/test.txt 的单词”）。
二、环境准备
（一）依赖安装
确保已安装 Python 3.8+，并通过以下命令安装核心依赖：
pip install langchain langgraph langchain-community spacy deepseek-ai
python -m spacy download en_core_web_sm   # 下载 spaCy 英文模型
（二）文件结构要求
项目需包含以下目录/文件（若缺失需手动创建）：
cet6_agent/
├── agent.py            # 核心 Agent 代码
├── cet6_5year/         # 存放 CET-6 真题文本的目录（需自行放入 .txt 文件）
│   ├── 2023_06.txt
│   ├── 2023_12.txt
│   └── ...
└── requirements.txt    # 依赖清单（可选，用于快速安装）
三、快速开始
（一）准备真题文本
将 CET-6 历年真题的文本内容保存为 .txt 文件，放入 cet6_5year/ 目录下（文件名可自定义，如 2024_06.txt）。
（二）运行 Agent
在终端进入项目根目录，执行：
python agent.py
（三）交互指令示例
启动后，Agent 会提示输入指令。例如：
你：提取 cet6_5year/test.txt 的单词
Agent: 正在处理 test.txt... 提取完成！结果已保存为 output.csv。
四、常见问题与解决
（一）报错：None of the expected files exist in the “cet6_5year/” directory
原因：cet6_5year/ 目录不存在，或目录下无 .txt 文件。解决步骤：
•  检查目录是否存在：在终端执行 ls cet6_5year/（Mac/Linux）或 dir cet6_5year\（Windows），确认目录和文件是否存在。
•  补全文件：若目录为空，将真题文本复制进去；若目录名错误（如写成 cet6_5years/），需修改代码中路径或重命名目录。
•  自定义路径：若文件存放在其他位置，需在交互时明确告知 Agent 完整路径（如 提取 /home/user/cet6_files/2024_06.txt 的单词）。
（二）警告：LangGraphDeprecatedSinceV10
原因：代码中使用了 LangGraph 旧版 API create_react_agent，该接口将在 V2.0 移除。
解决：打开 agent.py，将导入语句从：
from langgraph.prebuilt import create_react_agent
改为新版写法：
from langchain.agents import create_agent
五、进阶配置（可选）
•  更换大模型：若想替换 DeepSeek 为其他模型（如 OpenAI、通义千问），需修改 agent.py 中 LLM 初始化逻辑，并补充对应 API Key。
•  自定义过滤规则：在 spaCy 处理流程中，可调整停用词表或词频阈值（需修改 agent.py 中 NLP 处理函数）。
六、贡献与反馈
若发现 Bug 或有功能建议，欢迎提交 Issue 或 Pull Request。
