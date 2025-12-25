

from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages


class SearchState(TypedDict):
    messages: Annotated[list,add_messages]
    user_query: str
    search_query: str
    search_results: str
    final_anseer: str
    step: str
    
    