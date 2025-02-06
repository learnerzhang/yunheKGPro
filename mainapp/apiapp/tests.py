from langchain.tools import Tool
from langchain.agents import initialize_agent
from langchain_community.llms import Ollama

# 自定义工具：跳转到指定页面
def open_website(text: str) -> str:
    """
    根据用户输入返回跳转链接。
    """
    if "百度" in text:
        return "https://www.baidu.com"
    elif "谷歌" in text:
        return "https://www.google.com"
    else:
        return "暂不支持该网站"

# 将自定义工具添加到工具列表
tools = [
    Tool(
        name="OpenWebsite",
        func=open_website,
        description="用于跳转到指定网址。输入应包含目标网站名称，如'打开百度'。",
        return_direct=True  # 直接返回工具的结果
    )
]

# 初始化智能体
llm = Ollama(model="qwen2.5")  # 使用 OllamaLLM 替代 Ollama
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=False)

# 处理用户输入
def handle_user_input(user_input: str) -> str:
    """
    处理用户输入并返回跳转链接。
    """
    response = agent.run(user_input)
    return response

# 示例
if __name__ == "__main__":
    user_input = "帮我打开灌区网址"
    result = handle_user_input(user_input)
    print(result)  # 输出：https://www.baidu.com