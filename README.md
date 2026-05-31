# Episode 003 — Ai Agent with Tools

> [One sentence single takeaway from this project.]

## The Problem / The Question
What prompted this episode. What I was trying to understand or build. One to three sentences.

## What I Built
Plain English description of what was implemented. What it does and how it works at a high level.



web_search        — DuckDuckGo
wikipedia         — REST API
web_scraper       — fetch a URL, return clean text
file_reader       — read a local file
file_writer       — write/append to a local file
code_executor     — run Python, return output
Calculator        — eval a math expression



## What I Learned
- For this projet I did not use a framework like langchain so that i work through handling the loop, the tool dispatch, the message formatting — all the stuff that is the learning. LangChain makes sense later, when I already know what it's abstracting. Also I won´t even need langchain complexity for this small project I am building.
- [The thing that surprised me]
- The `code_executor` tool can be a dangerous one. I am running arbitrary Python that an LLM decided to write, so ofc in production I'd sandbox it (Docker, a subprocess with limits, etc.)
- I wanted to do `memory store` tool but realized it might be to complex for what i know, so I´ll learn to build it later :)

## How to Set Up
**Prerequisites**
- 

Install python package of choice, for this project I am experimenting with the fast package and project manager `uv`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```


Create a virtual environment, activate it and install the dependencies from `requirements.txt` (everything else used is standard library math, subprocess, pathlib, json...): 

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Check the installed packages

```bash
uv pip list
```

Copy the environment file and add your API keys:

```bash
cp .env.example .env
```


## Tech Used
- `uv` - python package manager, instead of pip 
- `python-dotenv` — loading API keys from `.env`
- `pydantic` — structured output validation
- `wikipedia`
- `duckduckgo-search`
- `beautifulsoup4`
- `requests`
- `rich` - Python library for rich text and beautiful formatting in the terminal


## References
- [uv project and package manager docs](https://docs.astral.sh/uv/getting-started/installation/)
- [beautiful soup library docs](https://pypi.org/project/beautifulsoup4/)
- [requests HTTP library docs](https://pypi.org/project/requests/)
- [rich library repo](https://github.com/Textualize/rich)
- [rich library docs](https://rich.readthedocs.io/en/latest/introduction.html)