# What models will I need? To know that ask the question: what data travels between my files?  Look at what your functions actually need return. The models are used in the return statement. 
# type annotation syntax in Python - variable: type declares the type of a variable
# From agent.py to tools.py: A tool runs and returns... what? 

from pydantic import BaseModel

class ToolResult(BaseModel):
    tool_name : str
    result : str 
    success : bool 
    error : str | None = None   #default of None






# From main.py → agent.py: What does the agent need to know to run? 
# class AgentConfig (Basemodel)
