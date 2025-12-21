import dotenv

from HelloAgentsLLM import HelloAgentsLLM
from PlanAndSolveAgent import PlanAndSolveAgent
from ReActAgent import ReactAgent
from ToolExecutor import ToolExecutor
from Tools import search, time_now

dotenv.load_dotenv()

# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':

    agent = PlanAndSolveAgent(
        llm_client=HelloAgentsLLM(),
    )

    agent.run("""
    
已知数列{an}，a≠0，若a1=3，2an+1-an=0， 则a6=
    """)