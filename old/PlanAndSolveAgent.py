import ast

from HelloAgentsLLM import HelloAgentsLLM

PLANNER_PROMPT_TEMPLATE = """
你是一个顶级的AI规划专家。你的任务是将用户提出的复杂问题分解成一个由多个简单步骤组成的行动计划。
请确保计划中的每个步骤都是一个独立的、可执行的子任务，并且严格按照逻辑顺序排列。
你的输出必须是一个Python列表，其中每个元素都是一个描述子任务的字符串。

问题: {question}

请严格按照以下格式输出你的计划,```python与```作为前后缀是必要的:
```python
["步骤1", "步骤2", "步骤3", ...]
```
"""

class Planner:
    def __init__(self,llm_client: HelloAgentsLLM):
        self.llm_client = llm_client

    def plan(self,question: str) -> list[str]:
        prompt = PLANNER_PROMPT_TEMPLATE.format(question=question)

        messages = [{"role": "user", "content": prompt}]

        print("--- 生成行动计划 ---")
        response_text = self.llm_client.think(messages=messages)
        if not response_text:
            print("❌ LLM 未返回任何响应，无法生成计划。")
            return []
        print(f"✅ 计划已生成:\n{response_text}")

        try:
            plan_str = response_text.split("```python")[1].split("```")[0].strip()
            plan = ast.literal_eval(plan_str)
            return plan if isinstance(plan, list) else []
        except (ValueError, SyntaxError, IndexError):
            print("❌ 计划格式不正确，无法解析。")
            return []
        except Exception as e:
            print("❌ 解析计划失败:", str(e))
            return []

EXECUTOR_PROMPT_TEMPLATE = """
你是一位顶级的AI执行专家。你的任务是严格按照给定的计划，一步步地解决问题。
你将收到原始问题、完整的计划、以及到目前为止已经完成的步骤和结果。
请你专注于解决“当前步骤”，并仅输出该步骤的最终答案，不要输出任何额外的解释或对话。

# 原始问题:
{question}

# 完整计划:
{plan}

# 历史步骤与结果:
{history}

# 当前步骤:
{current_step}

请仅输出针对“当前步骤”的回答:
"""


class Executor:
    def __init__(self,llm_client: HelloAgentsLLM):
        self.llm_client = llm_client

    def execute(self, question: str, plan: list[str]) -> str:

        history = []
        response_text = ""
        print("--- 正在执行计划 ---")

        for i, step in enumerate(plan):
            print(f"--- 执行步骤 {i+1}/{len(plan)} ---")
            prompt = EXECUTOR_PROMPT_TEMPLATE.format(
                question=question,
                plan=plan,
                history=history if history else "无",
                current_step=step
            )

            messages = [{"role": "user", "content": prompt}]

            response_text = self.llm_client.think(messages=messages) or ""

            history += f"步骤: {step}\n结果: {response_text.strip()}"
            print(f"✅ 步骤 {i + 1} 已完成，结果: {response_text}")

        final_answer = response_text
        return final_answer


class PlanAndSolveAgent:
    def __init__(self,llm_client: HelloAgentsLLM):
        self.planner = Planner(llm_client)
        self.executor = Executor(llm_client)
        self.llm_client = llm_client

    def run(self,question: str):
        print("=== 规划与执行代理启动 ===")
        plan = self.planner.plan(question)
        if not plan:
            print("❌ 未能生成有效的计划，终止执行。")
            return
        final_answer = self.executor.execute(question, plan)
        print(f"🎉 最终答案: {final_answer}")