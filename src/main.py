from rich.console import Console
from rich.panel import Panel
from agent import run_agent
from tools import TOOLS




console = Console ()

def main():

    #panel display using rich
    tool_names = list(TOOLS.keys())
    tool_list = "\n".join(f"• {name}" for name in tool_names)
    console.print(Panel.fit(f"\nTools Available:\n{tool_list}\n", title= "Zizo — Your personal AI Agent with Tools", border_style="bold blue"))
    print('"exit" or "quit" to terminate agent. Ask me anything!\n')

    messages = []

    while True:
        console.print()
        goal = console.input("[bold blue]→ [/bold blue]")
        if goal.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        else:
            messages.append({"role": "user", "content": goal})
            answer = run_agent(messages)
            console.print(f"\n[grey70]{answer}[/grey70]\n") #light grey

main()

