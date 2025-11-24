from utils.model_loader import ModelLoader
from prompt_library.prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessageState, END, START
from langgraph.prebuilt import ToolNode, tools_condition

'''
from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculation_tool import CalculationTool
from tools.currency_conversion_tool import CurrencyConversionTool
'''



class GraphBuilder():

    def __init__(self):
        self.system_prompt = SYSTEM_PROMPT

    def agent_function(self, state: MessageState):
        user_query = state["messages"]
        input_query = [self.system_prompt] + user_query
        response = self.llm_with_tools.invoke(input_query)
        return {"messages": [response]}
 

    def build_graph(self):
        graph_builder = StateGraph(MessageState)
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges("agent", tools_condition)
        graph_builder.add_edge("agent", "tools")
        graph_builder.add_edge("tools", END)
        self.graph = graph_builder.compile()
        return self.graph

    #called by graph() instance of GraphBuilder class from app.py
    def __call__(self):
        return self.build_graph()