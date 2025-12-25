import math

import dotenv

from HelloAgentsLLM import HelloAgentsLLM
from PlanAndSolveAgent import PlanAndSolveAgent
from ReActAgent import ReactAgent
from ReflectionAgent import ReflectionAgent
from ToolExecutor import ToolExecutor
from Tools import search, time_now

dotenv.load_dotenv()


if __name__ == '__main__':

    # print(find_primes(int(math.pow(10,7))))


    agent = HelloAgentsLLM()
    response = agent.think([
        {"role": "system", "content": "You are a helpful assistant that writes Python code."},
        {"role": "user", "content": "写一个快速排序算法"}
    ])

    print("LLM响应内容:")
    print(response)
