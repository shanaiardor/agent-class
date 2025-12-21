import os
from typing import List, Dict

from dotenv import load_dotenv
from exa_py import Exa
from openai import OpenAI

load_dotenv()

class HelloAgentsLLM:
    def __init__(self, model: str =  None,apiKey: str = None, baseUrl: str = None, timeout: int = None):

        self.model = model or os.getenv("LLM_MODEL_ID")
        self.apiKey = apiKey or os.getenv("LLM_API_KEY")
        self.baseUrl = baseUrl or os.getenv("LLM_BASE_URL")
        self.timeout = timeout or int(os.getenv("LLM_TIMEOUT", "60"))
        if not all([self.model, self.apiKey, self.baseUrl, self.timeout]):
            raise ValueError("Missing required configuration for HelloAgentsLLM")

        self.client = OpenAI(api_key=self.apiKey, base_url=self.baseUrl, timeout=self.timeout)

    def think(self, messages: List[Dict[str,str]], temperature: float = 0) -> str:
        print(f"🧠 正在调用 {self.model} 模型...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,
            )

            print("✅ 大语言模型响应成功:")
            collected_content = []
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                print(content,end="",flush=True)
                collected_content.append(content)
            print()
            return "".join(collected_content)
        except Exception as e:
            print("❌ 大语言模型响应失败:", str(e))
            raise None



#
# if __name__ == "__main__":
#     result = search("最新型号的华为手机是什么？")
#     print("搜索结果:")
#     print(result)
#     # try:
#     #     llmClient = HelloAgentsLLM()
#     #     exampleMessages = [
#     #         {"role": "system", "content": "You are a helpful assistant that writes Python code."},
#     #         {"role": "user", "content": "写一个快速排序算法"}
#     #     ]
#     #     print("--- 调用LLM ---")
#     #     responseText = llmClient.think(exampleMessages)
#     #     if responseText:
#     #         print("--- LLM响应内容 ---")
#     #         print(responseText)
#     # except Exception as e:
#     #     print(e)
#     #
