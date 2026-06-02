from anthropic import Anthropic
from dotenv import load_dotenv
from tools import TOOL_SCHEMAS, run_tool

load_dotenv()

def run_agent(goal: str) -> str:
    client = Anthropic() #our client
    messages = [{"role": "user", "content": goal}]  #our history

    #loop until claude stops asking for tools
    while True:
        response = client.messages.create(  #response block
            model="claude-haiku-4-5",
            max_tokens=1024,
            tools=TOOL_SCHEMAS,
            messages=messages
        )

        #checks if Claude is done without calling a tool
        if response.stop_reason != "tool_use": 
            return response.content[0].text

        # append Claude's response to messages list history
        messages.append({"role": "assistant", "content": response.content})

        # run the tools and collect results
        tool_results = [] #format Anthropic requires when you send tool results back, tells Anthropic this is a tool result, not a user message. We will add this to history content
        for block in response.content: #response.content is a list and contains multiple blocks.
            if block.type == "tool_use": #claude is using a tool
                result = run_tool(block.name, block.input) # Our run_tool function - the tool claude decided to call from the schema and the arguments 
                tool_results.append({
                    "type": "tool_result", 
                    "tool_use_id": block.id,
                    "content": result.result
                })

        # append tool results back to messages
        messages.append({"role": "user", "content": tool_results})

'''
Test:
print(run_agent("What is 25 * 48?"))
'''







