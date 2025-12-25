import re
import inspect
from pyexpat.errors import messages

from HelloAgentsLLM import HelloAgentsLLM
from ToolExecutor import ToolExecutor

# ReAct 提示词模板
REACT_PROMPT_TEMPLATE = """
请注意，你是一个有能力调用外部工具的智能助手。

可用工具如下:
{tools}

请严格按照以下格式进行回应:

Thought: 你的思考过程，用于分析问题、拆解任务和规划下一步行动。
Action: 你决定采取的行动，必须是以下格式之一:
- `{{tool_name}}[{{tool_input}}]`:调用一个可用工具。
- `Finish[最终答案]`:当你认为已经获得最终答案时。
- 当你收集到足够的信息，能够回答用户的最终问题时，你必须在Action:字段后使用 finish(answer="...") 来输出最终答案。

现在，请开始解决以下问题:
Question: {question}
History: {history}
"""


class ReactAgent:
    def __init__(self, llm_client: HelloAgentsLLM, tool_executor: ToolExecutor,max_steps: int = 5):
        self.llm_client = llm_client
        self.tool_executor = tool_executor
        self.max_steps = max_steps
        self.history = []

    def run(self, question: str):
        self.history = []
        current_step = 0
        while current_step < self.max_steps:
            current_step += 1
            print(f"--- 第 {current_step} 步 ---")

            tools_desc = self.tool_executor.getAvailableTools()
            prompt = REACT_PROMPT_TEMPLATE.format(
                tools=tools_desc,
                question=question,
                history="\n".join(self.history)
            )

            messages = [{"role": "user", "content": prompt}]
            response_text = self.llm_client.think(messages=messages)

            if not response_text:
                print("❌ LLM 未返回任何响应，终止执行。")
                break

            thought,action = self._parse_output(response_text)

            if thought:
                print(f"💭 思考: {thought}")

            if not action:
                print("❌ 未能解析出 Action，终止执行。")
                break

            if action.startswith("Finish"):
                final_answer = re.match(r"Finish\[(.*)\]", action).group(1)
                print(f"🎉 最终答案: {final_answer}")
                return final_answer

            tool_name,tool_input = self._parse_action(action)
            if not tool_name:
                continue

            print(f"--- 执行工具 --- {tool_name} with input: {tool_input}")

            tool_function = self.tool_executor.getTool(tool_name)
            if not tool_function:
                print(f"❌ 未找到工具 '{tool_name}'，终止执行。")
                break
            else:
                sig = inspect.signature(tool_function)
                parmas = list(sig.parameters.keys())
                if len(parmas) == 0:
                    observation = tool_function()
                else:
                    observation = tool_function(tool_input)
                print(f"👀 观察: {observation}")

                self.history.append(f"Action: {action}\nObservation: {observation}")
        else:
            print("❌ 达到最大步骤数，未能得出最终答案。")
        return None


    def _parse_output(self, text:str):
        thought_match = re.search(r"Thought:(.*)",text)
        action_match = re.search(r"Action:(.*)",text)
        thoutght = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None
        return thoutght, action

    def _parse_action(self, action_text:str):
        match = re.match(r"(\w+)\[(.*)\]", action_text)
        if match:
            return match.group(1),match.group(2)
        return None,None




if __name__ == '__main__':
    from Tools import search, time_now

    tools_executor = ToolExecutor()
    tools_executor.registerTool(
        name="WebSearch",
        descrption="使用此工具进行网页搜索以获取最新的信息。",
        func=search
    )
    tools_executor.registerTool(
        name="time",
        descrption="使用此工具获取当前的日期和时间。 无参数",
        func=time_now
    )

    agent = ReactAgent(
        llm_client=HelloAgentsLLM(),
        tool_executor=tools_executor,
        max_steps=10
    )
    agent.run("金铲铲 英雄联盟传奇赛季 什么阵容最牛？")
