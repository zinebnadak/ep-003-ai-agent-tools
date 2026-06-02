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
from ddgs import DDGS
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


def file_writer(filepath:str, content: str, mode: str = "write") -> ToolResult: # the mode can either be append or write, writing default
    try: 
        normalized_path = Path(filepath).resolve()
        flag = "a" if mode == "append" else "w"
        with open(normalized_path, flag) as f:
            f.write(content)
            return ToolResult(tool_name="file_writer", result=f"Sucessfully written to {filepath}", success = True, error = None)
    
    except Exception as e:
            return ToolResult(tool_name="file_writer", result="", success = False, error = str(e))


'''
Supports both writing (overwriting) and appending
print(file_writer("/Users/nadak/ep-003-ai-agent-tools/docs/notes.md", "hejdå", "append"))
'''


def web_search(query: str):
    try: 
        lines = []
        results = DDGS().text(query, max_results = 3)
        for result in results:
            lines.append(f"{result['title']}\n{result['body']}\n{result['href']}")
        formatted_result = "\n\n".join(lines)
        return ToolResult(tool_name="web_search", result=f'Results for "{query}": {formatted_result}', success = True, error = None) 
    except Exception as e:
        return ToolResult(tool_name="web_search", result="", success = False, error = str(e))

'''
The \n characters will render as actual newlines when Claude processes it
print(web_search("How old can a cat be?"))
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
        "description" : "Read a local file and return its contents. Use when the user asks to read, summarise or analyse a file.",
        "input_schema" : {
            "type" : "object",
            "properties" : {    
            "filepath" : {"type": "string"} #only one property  
            },
            "required": ["filepath"]
        }
    },
    {
        "name" : "file_writer",
        "description" : "Write or append text to a local file. Use when the user wants to save, create or add to a file.",
        "input_schema" : {
            "type" : "object",
            "properties" : {    
            "filepath" : {"type": "string"},
            "content" : {"type": "string"},
            "mode" : {"type": "string"}
            },
            "required": ["filepath"],
            "required": ["content"]
        }
    }
    {
        "name" : "web_search",
        "description": "Search the web with DuckDuckGo. Use this for current information, news, prices, or anything that requires up-to-date knowledge.",
        "input_schema" : {
            "type" : "object",
            "properties" : {    
            "query" : {"type": "string"}
            },
            "required": ["query"]
        }
    }

]

#if the user says "save this to a file" it writes, if the user says "add this to my notes" it appends







'''
Dispatch table maps tool names to functions so run_tool() can look them up
'''
TOOLS = {
    "calculator" : calculator,
    "file_reader" : file_reader,
    "file_writer" : file_writer,
    "web_search" : web_search,
}






'''
This function is used to run a tool
'''
def run_tool(name, inputs) -> ToolResult:
    requested_tool = TOOLS[name]    #look up the tool by name form th dictionary TOOLS
    return requested_tool(**inputs) #run requested_tool function with the inputs arguments, **inputs unpacks a dictionary into keyword arguments.






