from anthropic import Anthropic
from dotenv import load_dotenv
from tools import TOOL_SCHEMAS, run_tool
import time 
from rich.console import Console
console = Console()

load_dotenv()

#*args = positional arguments (like block.name, block.input)
#**kwargs = keyword arguments (like model="claude-haiku-4-5")
#fn is the tool function

PINK = "\033[38;5;125m"   
RESET = "\033[0m"

def spinner(message: str, fn, *args, **kwargs): 
    console.print(f"[#99004c] {message}...[/#99004c]", end="", highlight=False)
    start = time.time()
    result = fn(*args, **kwargs)
    elapsed = time.time() - start
    console.print(f"[#99004c] done in {elapsed:.1f}s[/#99004c]", highlight=False)
    return result

def run_agent(messages: list) -> str:
    client = Anthropic() #our client

    #loop until claude stops asking for tools
    while True:
        #response block
        response = spinner("\nThinking",client.messages.create,  
            model="claude-haiku-4-5",
            max_tokens=1024,
            tools=TOOL_SCHEMAS,
            messages=messages
        ) #here the spinner takes this message as parameter and runs as a function on this message - *kawgs

        #checks if Claude is done without calling a tool
        if response.stop_reason != "tool_use":
            messages.append({"role": "assistant", "content": response.content}) 
            return response.content[0].text

        # append Claude's response to messages list history
        messages.append({"role": "assistant", "content": response.content})

        # run the tools and collect results
        tool_results = [] #format Anthropic requires when you send tool results back, tells Anthropic this is a tool result, not a user message. We will add this to history content
        for block in response.content: #response.content is a list and contains multiple blocks.
            if block.type == "tool_use": #claude is using a tool
                block_input_value = list(block.input.values())[0] #get block input value
                result = spinner(f'Searching with {block.name} for "{block_input_value}"', run_tool, block.name, block.input) # Our run_tool function. Here also the spinner takes this as parameter and runs as a function on this result - *args
                tool_results.append({
                    "type": "tool_result", 
                    "tool_use_id": block.id,
                    "content": result.result
                })

        # append tool results back to messages
        messages.append({"role": "user", "content": tool_results})










