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

def calculator(expression: str) -> ToolResult:      #the user enters an expression, and from this function we will get out predefined model: name, result, success (or error)
    try:
        answer = str(eval(expression))
        return ToolResult(tool_name = "calculator", result = answer, success = True, error = None)   #arguments
    except Exception as e:
        return ToolResult(tool_name = "calculator", result = "Failed to calculate expression.",success = False, error = str(e))


expression_input = str(input("Enter an expression: "))
print(calculator(expression_input))




# Schemas are what the LLM reads to know tools exist to choose from
TOOL_SCHEMAS =[

]



TOOLS = {
    "calculator": calculator
}



function to run a tool
def run_tool(name, inputs) -> ToolResult:





