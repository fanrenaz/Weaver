import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# --- 1. 加载环境变量 ---
# load_dotenv() 会自动查找项目根目录下的 .env 文件并加载
print("Loading environment variables from .env file...")
load_dotenv()

# 从环境变量中获取配置
# os.getenv() 在找不到时会返回 None，这很安全
api_base = os.getenv("OPENAI_API_BASE")
api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL_NAME")  # 可选

# --- 2. 检查配置并初始化LLM客户端 ---
print("Initializing ChatOpenAI client...")

if not api_base:
    # 如果没有设置自定义endpoint，就使用默认的OpenAI服务
    print("OPENAI_API_BASE not set, using default OpenAI endpoint.")
    llm = ChatOpenAI(api_key=api_key, model=model_name if model_name else "gpt-3.5-turbo")
else:
    # 如果设置了自定义endpoint，就使用它
    print(f"Using custom endpoint: {api_base}")
    llm = ChatOpenAI(
        base_url=api_base,
        api_key=api_key,
        model=(
            model_name if model_name else None
        ),  # 如果是本地模型，可能不需要指定模型名称，或者需要指定一个特定的名称
    )

print("ChatOpenAI client initialized successfully.")

# --- 3. 进行一次简单的调用测试 ---
print("\n--- Testing LLM Invocation ---")
try:
    # 我们不再使用复杂的Graph，直接测试LLM调用，这更直接
    message = HumanMessage(
        content="Hello! Please reply with a short confirmation that you received this message."
    )
    response = llm.invoke([message])

    print("\n[SUCCESS] LLM call successful!")
    print("Response from model:")
    print("--------------------")
    print(response.content)
    print("--------------------")

except Exception as e:
    print("\n[ERROR] An error occurred during the LLM call.")
    print("Please check your endpoint, API key, and network connection.")
    print(f"Error details: {e}")
