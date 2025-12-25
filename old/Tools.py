import os

from exa_py import Exa


def search(query: str) -> str:
    print(f"🔍 正在执行 [SerpApi] 网页搜索: {query}")

    try:
        api_key = os.getenv("EXA_API_KEY")
        exa = Exa(api_key=api_key)
        result = exa.search(query,num_results=1,type="deep")
        return result.context
    except Exception as e:
        print("❌ 网页搜索失败:", str(e))
        return ""

def time_now() -> str:
    from datetime import datetime
    print("🕒 正在获取当前时间")
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return f"当前时间是: {current_time}"

