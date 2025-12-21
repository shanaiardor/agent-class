from typing import List, Dict, Any, Optional


class Memory:
    """
    一个简单的短期记忆类，用于存储和检索信息。
    """

    def __init__(self):
        self.records: List[Dict[str,Any]] = []

    def add_record(self, record_type: str,content: str):
        """
        向记忆中添加一条新记录。

        参数:
        - record_type (str): 记录的类型 ('execution' 或 'reflection')。
        - content (str): 记录的具体内容 (例如，生成的代码或反思的反馈)。
        """
        record = {
            "type": record_type,
            "content": content
        }
        self.records.append(record)
        print("🧠 记忆已更新，新增一条 '{record_type}' 记录。")

    def get_trajectory(self) -> str:
        """
        获取当前的记忆轨迹，按时间顺序返回所有记录。

        返回:
        - trajectory (str): 按时间顺序排列的所有记录内容。
        """
        trajectory_parts = ""
        for record in self.records:
            if record["type"] == "execution":
                trajectory_parts.append(f"--- 上一轮尝试 (代码) ---\n{record['content']}")
            if record["type"] == "reflection":
                trajectory_parts.append(f"--- 上一轮反思 (反馈) ---\n{record['content']}")
        return "\n\n".join(trajectory_parts)

    def get_last_execution(self) -> Optional[str]:
        """
        获取最近一次的执行记录内容。

        返回:
        - last_execution (str): 最近一次的执行记录内容，如果没有则返回空字符串。
        """
        for record in reversed(self.records):
            if record["type"] == "execution":
                return record["content"]
        return None