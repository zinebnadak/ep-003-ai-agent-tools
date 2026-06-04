'''
7 tools:
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
import requests
from bs4 import BeautifulSoup
import subprocess 
from datetime import date


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


def web_search(query: str) -> ToolResult:
    try:
        dated_query = f"{query} {date.today()}"
        lines = []
        results = DDGS().text(dated_query, max_results=3)
        for result in results:
            lines.append(f"{result['title']}\n{result['body']}\n{result['href']}")
        formatted_result = "\n\n".join(lines)
        return ToolResult(tool_name="web_search", result=f'Results for "{query}": {formatted_result}', success=True, error=None)
    except Exception as e:
        return ToolResult(tool_name="web_search", result="", success=False, error=str(e))

'''
The \n characters will render as actual newlines when Claude processes it
print(web_search("How old can a cat be?"))
'''


def web_scraper(url: str) -> ToolResult:
    try: 
        response = requests.get(url)
        bad_html = response.text
        parsed = BeautifulSoup(bad_html, "html.parser")
        text = parsed.get_text()
        lines = [line.strip() for line in text.splitlines() if line.strip()] #if line.strip() means if the line is not empty after stripping whitespace
        clean_response = "\n".join(lines)
        return ToolResult(tool_name="web_scraper", result=f'Content results for "{url}": {clean_response}', success = True, error = None) 
    
    except Exception as e:
        return ToolResult(tool_name="web_scraper", result="", success = False, error = str(e)) 

'''
Small issue: the \n dont render as newlines, but claude will be able to read it anyway...
print(web_scraper("hts://github.com/zinebnadak"))
'''

def wikipedia(topic: str) -> ToolResult:
    
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
        headers = {"User-Agent": "EP3Agent/1.0 (educational project; python)"} #bcs of robot policy
        response = requests.get(url, headers=headers)
        data = response.json()
        summary = data["extract"]
        return ToolResult(tool_name="wikipedia", result=f"{summary}", success=True, error=None)
    except Exception as e:
        return ToolResult(tool_name="wikipedia", result="", success=False, error=str(e))

'''
Same here, i get \n
print(wikipedia("zinebnadak"))
'''



def code_executor(code: str) -> ToolResult:

    try: 
        extracted = subprocess.run(["python3", "-c", code], capture_output = True, text = True, timeout=15)  # -c run a string of code directly instead of a file ,subprocess needs a list
        result = extracted.stdout #stout prints the output
        error = extracted.stderr if extracted.stderr else None #stderr is where all errors in python go
        return ToolResult(tool_name="code_executor", result=extracted.stdout, success=extracted.returncode == 0, error=error)
    
    except subprocess.TimeoutExpired:
        return ToolResult(tool_name="code_executor", result="", success=False, error="Code timed out after 15 seconds")
    
    except Exception as e:
        return ToolResult(tool_name="code_executor", result="", success=False, error=str(e))

'''
Test timeout, stdout and stderr:
print(code_executor("while True: pass"))
print(code_executor("print('hello')"))          
print(code_executor("1/0"))
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
            "required": ["filepath", "content"],
        }
    },
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
    },
    {
        "name" : "web_scraper",
        "description": "Fetch a URL and return its readable text content. Use this when you have a specific URL and need the full page content.",
        "input_schema" : {
            "type" : "object",
            "properties" : {    
            "url" : {"type": "string"}
            },
            "required": ["url"]
        }
    },
    {
        "name" : "wikipedia",
        "description": "fetches a Wikipedia article summary of a specific topic",
        "input_schema" : {
            "type" : "object",
            "properties" : {    
            "topic" : {"type": "string"}
            },
            "required": ["topic"]
        }
    },
    {
        "name" : "code_executor",
        "description": "runs a Python file and returns its output",
        "input_schema" : {
            "type" : "object",
            "properties" : {    
            "code" : {"type": "string"}
            },
            "required": ["code"]
        }
    }

]


'''
Dispatch table maps tool names to functions so run_tool() can look them up
'''
TOOLS = {
    "calculator" : calculator,
    "file_reader" : file_reader,
    "file_writer" : file_writer,
    "web_search" : web_search,
    "web_scraper" : web_scraper,
    "wikipedia" : wikipedia,
    "code_executor" : code_executor
}


'''
This function is used to run a tool
'''
def run_tool(name, inputs) -> ToolResult:
    requested_tool = TOOLS[name]    #look up the tool by name form th dictionary TOOLS
    return requested_tool(**inputs) #run requested_tool function with the inputs arguments, **inputs unpacks a dictionary into keyword arguments.






