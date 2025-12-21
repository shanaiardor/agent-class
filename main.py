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


    agent = ReflectionAgent(
        llm_client=HelloAgentsLLM(),
        max_iterations=3
    )

    agent.run("编写一个Python函数，找出1到n之间所有的素数 (prime numbers)。")
