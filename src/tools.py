'''
7 tools in total:
calculator
file_reader
file_writer
web_search
web_scraper
wikipedia
code_executor
'''


from models import ToolResult
from pathlib import Path
import json

def calculator(expression: str) -> ToolResult:      #the user enters an expression, and from this function we will get out predefined model: name, result, success (or error)
    try:
        answer = str(eval(expression))
        return ToolResult(tool_name = "calculator", result = answer, success = True, error = None)   #arguments
    except Exception as e:
        return ToolResult(tool_name = "calculator", result = "Failed to calculate expression.",success = False, error = str(e))

'''
Test:
expression_input = str(input("Enter an expression: "))
print(calculator(expression_input))
'''


def file_reader(filepath: str) -> ToolResult:
    try:
        normalized_path = Path(filepath).resolve()  #normalizes the path to absolute path, resolves relative to where you're running the script from,
        with open(normalized_path, "r") as f:
            content = f.read()
            return ToolResult(tool_name="file_reader", result=content, success = True, error = None)
    
    except Exception as e:
        return ToolResult(tool_name="file_reader", result="Failed to read file", success = False, error = str(e))
        

'''
user must provide the full path
print(file_reader("/Users/nadak/ep-003-ai-agent-tools/docs/notes.md"))
'''




'''
Schemas are what the LLM reads to know tools exist to choose from
The schema is a list sent to Anthropic, and each tool has its own dictionary with the keys: name, description and an input_schema with the keys: type, properties and required
'''
TOOL_SCHEMAS = [
    {
        "name" : "calculator",
        "description" : "This tool calculates an expression",
        "input_schema" : {
            "type" : "object",
            "properties" : { #properties defines possible arguments and their types.     
            "expression" : {"type": "string"} #only one property  
            },
            "required": ["expression"] #arguments that can't be missing when calling the tool goes to required
        }
    },
    {
        "name" : "file_reader",
        "description" : "This tool opens a file and reads it",
        "input_schema" : {
            "type" : "object",
            "properties" : {    
            "filepath" : {"type": "string"} #only one property  
            },
            "required": ["filepath"]
        }
    }

]





'''
Dispatch table maps tool names to functions so run_tool() can look them up
'''
TOOLS = {
    "calculator" : calculator,
    "file_reader" : file_reader
}






'''
This function is used to run a tool
'''
def run_tool(name, inputs) -> ToolResult:
    requested_tool = TOOLS[name]    #look up the tool by name form th dictionary TOOLS
    return requested_tool(**inputs) #run requested_tool function with the inputs arguments, **inputs unpacks a dictionary into keyword arguments.






