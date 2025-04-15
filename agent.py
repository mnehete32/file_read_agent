import os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph
from typing import Annotated, Sequence
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import json
from tools import FileReadTool
from pydantic import BaseModel

class AgentState(BaseModel):
    messages: Annotated[Sequence[BaseMessage], add_messages]

class SimpleAgent:
    def __init__(self):
        self.console = Console()
        self.console.print(Panel.fit("[bold green]Simple Agent[/bold green]", title="Agent", border_style="green"))

        self.model = ChatGoogleGenerativeAI(
                        model="gemini-2.5-pro-exp-03-25",
                        google_api_key=os.getenv("GEMINI_API_KEY"),
                        temperature=0.7
                )
        self.tools = [FileReadTool()]
        self.model = self.model.bind_tools(tools = self.tools)
        workflow = StateGraph(AgentState)
        workflow.add_node("user_input", self._get_user_input)
        workflow.add_node("model_response", self._get_model_response)
        workflow.add_node("tool_use", self._get_tool_use)
        workflow.set_entry_point("user_input")
        workflow.add_edge("user_input", "model_response")
        workflow.add_edge("tool_use", "model_response")
        workflow.add_conditional_edges(
            "model_response",
            self._check_tool_use,{
                "tool_use":  "tool_use",
                "user_input": "user_input"
            }
        )

        self.agent = workflow.compile()
        # code to print the graph of the workflow, uncomment for debugging
        # print(self.agent.get_graph().draw_mermaid())
    def run(self):
        return self.agent.invoke({"messages": [AIMessage(content="Hello! How can I assist you today?")]})
    
    def _get_user_input(self, state: AgentState) -> AgentState:
        self.console.print("[bold blue]User Input[/bold blue]")
        user_input = self.console.input("[bold blue]>[/bold blue]")
        self.console.print(Panel.fit("[bold blue]" + user_input + "[/bold blue]", title="User Input", border_style="bold blue"))
        
        return {"messages": [HumanMessage(content=user_input)]}
    
    def _get_model_response(self, state: AgentState) -> AgentState:
        messages = [

            SystemMessage(content = [{
                              "type": "text",
                              "text": "You are a helpful assistant that can read files.",
                              "cache_control": {
                                  "type": "ephemeral",
                              }
                          }]),
                          HumanMessage(content=f"Working directory: {os.getcwd()}"),
        ] + state.messages 
        response = self.model.invoke(messages)
    
        if response.tool_calls:
            self.console.print(Panel.fit("[yellow]" + str(response.tool_calls) + "[/yellow]", title="AI", border_style="yellow"))
            pass
        else:
            self.console.print(Panel.fit(Markdown(str(response.content)), title="AI", border_style="yellow"))
        
        return {"messages": response}
    

    def _get_tool_use(self, state: AgentState) -> AgentState:
        tools_by_name = {tool.name: tool for tool in self.tools}
        response = []
    
        for tool_call in state.messages[-1].tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_call_id = tool_call["id"]
            tool = tools_by_name.get(tool_name)
        try:
            tool_result = tool._run(**tool_args)
            response.append(ToolMessage(content=tool_result, name= tool_name, tool_call_id = tool_call_id))

            # self.console.print(Panel.fit("[green]" + tool_result + "[/green]", title="Tool Result", border_style="green"))
        except Exception as e:
            # self.console.print(Panel.fit("[green]Error: " + str(e) + "[/green]", title="Tool Result", border_style="green"))
            response.append(ToolMessage(content="Error: " +str(e), name= "Error", tool_call_id = tool_call_id))
        return {"messages": response}

    def _check_tool_use(self, state: AgentState) -> str:
            if state.messages[-1].tool_calls:
                return "tool_use"
            return "user_input"


if __name__ == "__main__":
    load_dotenv()
    agent = SimpleAgent()
    agent.run()
