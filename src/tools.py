'''
7 tools in total:
web_search
wikipedia
web_scraper
file_reader
file_writer
code_executor
calculator
'''


from models import ToolResult
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
    }
]





'''
Dispatch table maps tool names to functions so run_tool() can look them up
'''
TOOLS = {
    "calculator": calculator
}






'''
This function is used to run a tool
'''
def run_tool(name, inputs) -> ToolResult:
    requested_tool = TOOLS[name]    #look up the tool by name form th dictionary TOOLS
    return requested_tool(**inputs) #run requested_tool function with the inputs arguments






