import re
import shutil

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.cells import cell_len

from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style

from agent import run_agent
from tools import TOOLS

console = Console()


OWL = r"""
,_,
(o,o)
{`"'}
-"-"-
"""

TOOL_UI = {
    "calculator": "🧮 Calculator",
    "file_reader": "📂 Analyze files",
    "file_writer": "📝 Write files",
    "web_search": "🔍 Search web",
    "web_scraper": "🕸  Scrape the web",
    "wikipedia": "📚 Wikipedia",
    "code_executor": "🐍 Run Python",
}

toolbar_style = Style.from_dict({
    "bottom-toolbar": "noreverse bg:default fg:#444444",
    "": "fg:#808080",  # typed input text color (grey50)
})


def make_rule():
    width = shutil.get_terminal_size().columns
    return HTML(f'<ansibrightblack>{"─" * width}</ansibrightblack>')


def render_welcome():
    # ---- left column lines ----
    left_lines = [
        "",
        "My first AI",
        "agent with",
        "tools.",
        "",
        *OWL.strip("\n").splitlines(),
        "",
    ]

    # ---- right column lines ----
    right_lines = [
        "[bold #99004c]What I can Do[/bold #99004c]",
        "",
        *TOOL_UI.values(),
    ]

    # pad both columns to equal height
    height = max(len(left_lines), len(right_lines))
    left_lines += [""] * (height - len(left_lines))
    right_lines += [""] * (height - len(right_lines))

    grid = Table.grid(padding=(0, 1), expand=False)
    grid.add_column(justify="left", width=14, no_wrap=True, overflow="crop")
    grid.add_column(justify="left", no_wrap=True)
    grid.add_column(justify="left", no_wrap=True, overflow="crop")

    for l, r in zip(left_lines, right_lines):
        l_style = "bold #99004c"
        l_text = Text(l, style=l_style) if l else Text("")
        bar = Text("│", style="#99004c")
        r_text = Text.from_markup(r) if r else Text("")
        grid.add_row(l_text, bar, r_text)

    header = Text("Made by Nadak", style="grey50")

    # widest line in each column (strip markup tags for an accurate length)
    plain_right = [re.sub(r"\[/?[^\]]+\]", "", r) for r in right_lines]
    left_w = max((cell_len(l) for l in left_lines), default=0)
    right_w = max((cell_len(r) for r in plain_right), default=0)
    content_w = left_w + right_w + 1 + 6  # +1 divider, +6 padding/borders
    panel_width = max(content_w, console.width // 2)

    console.print(Panel(
        grid,
        title=header,
        title_align="left",
        border_style="#99004c",
        subtitle='[grey50]/Type "exit" or "quit" to terminate agent[/grey50]',
        subtitle_align="right",
        width=panel_width,
    ))



def main():
    render_welcome()

    messages = []

    while True:
        console.rule(style="grey50")  # top line
        try:
            goal = prompt(
                HTML('<ansibrightblack>❯ </ansibrightblack>'),
                bottom_toolbar=make_rule(),  # bottom line while typing
                style=toolbar_style,
            )
        except (EOFError, KeyboardInterrupt):
            console.print("\nGoodbye!")
            break
        console.rule(style="grey50")  # keep bottom line after submit

        if goal.lower().strip() in ("exit", "quit"):
            console.print("[grey50]Goodbye![/grey50]")
            break
        if not goal.strip():
            continue

        messages.append({"role": "user", "content": goal})
        answer = run_agent(messages)
        console.print(f"\n[#99004c]{answer}[/#99004c]\n")


if __name__ == "__main__":
    main()