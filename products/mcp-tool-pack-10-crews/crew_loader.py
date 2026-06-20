#!/usr/bin/env python3
"""
Load and run any crew from the MCP Tool Pack YAML configs.

Usage:
    export XAI_API_KEY=...   # or OPENAI_API_KEY
    python crew_loader.py crews/04_marketing_launch_crew.yaml "Launch my Notion template at $29"
    python crew_loader.py crews/01_research_crew.yaml --topic "AI prompt packs for law students"
"""

import argparse
import os
import sys
from pathlib import Path

import yaml
from crewai.tools import tool

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


@tool("Web Search")
def web_search(query: str) -> str:
    """Search the web for current information."""
    try:
        from ddgs import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=7))
            return "\n".join(
                f"- {r.get('title', '')}: {r.get('body', '')} ({r.get('href', '')})"
                for r in results
            ) or "No results"
    except Exception as e:
        return f"Search error: {e}"


@tool("File Read")
def file_read(path: str) -> str:
    """Read a local text file and return its contents."""
    try:
        p = Path(path).expanduser().resolve()
        if not p.is_file():
            return f"File not found: {p}"
        return p.read_text(encoding="utf-8", errors="replace")[:12000]
    except Exception as e:
        return f"Read error: {e}"


TOOL_REGISTRY = {
    "web_search": web_search,
    "file_read": file_read,
}


def resolve_tools(tool_names):
    """Map YAML tool names to CrewAI tool instances."""
    if not tool_names:
        return []
    resolved = []
    for name in tool_names:
        tool_obj = TOOL_REGISTRY.get(name)
        if tool_obj:
            resolved.append(tool_obj)
        else:
            print(f"Warning: unknown tool '{name}' — skipping", file=sys.stderr)
    return resolved


def get_llm():
    from crewai import LLM

    xai = os.getenv("XAI_API_KEY")
    oai = os.getenv("OPENAI_API_KEY")
    if xai and not xai.startswith("your_"):
        return LLM(
            model=os.getenv("XAI_MODEL", "grok-4"),
            api_key=xai,
            base_url="https://api.x.ai/v1",
            temperature=0.65,
        )
    if oai:
        return LLM(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), api_key=oai)
    sys.exit("Set XAI_API_KEY or OPENAI_API_KEY in environment.")


def load_crew(config_path: Path, user_input: str):
    from crewai import Agent, Crew, Process, Task

    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    llm = get_llm()
    agents = []
    agent_map = {}

    for a in cfg.get("agents", []):
        agent_tools = resolve_tools(a.get("tools", []))
        agent = Agent(
            role=a["role"],
            goal=a.get("goal", f"Execute tasks as {a['role']}"),
            backstory=a.get("backstory", f"Expert {a['role']}."),
            tools=agent_tools or None,
            llm=llm,
            verbose=a.get("verbose", True),
        )
        agents.append(agent)
        agent_map[a["role"]] = agent

    tasks = []
    for t in cfg.get("tasks", []):
        agent = agent_map.get(t.get("agent"))
        if not agent and agents:
            agent = agents[min(len(tasks), len(agents) - 1)]
        desc = t.get("description", t) if isinstance(t, dict) else str(t)
        if isinstance(t, dict):
            desc = f"{desc}\n\nUser context:\n{user_input}"
            task = Task(
                description=desc,
                expected_output=t.get("expected_output", "Structured output in Markdown."),
                agent=agent,
            )
        else:
            task = Task(
                description=f"{desc}\n\nUser context:\n{user_input}",
                expected_output="Structured output in Markdown.",
                agent=agent,
            )
        tasks.append(task)

    crew = Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )
    return crew, cfg.get("name", config_path.stem)


def main():
    parser = argparse.ArgumentParser(description="Run an MCP Tool Pack crew from YAML")
    parser.add_argument("config", type=Path, help="Path to crew YAML file")
    parser.add_argument("input", nargs="?", default="", help="Topic or task description")
    parser.add_argument("--topic", type=str, help="Alias for input")
    args = parser.parse_args()

    user_input = args.topic or args.input or "General run — use best judgment."
    if not args.config.exists():
        sys.exit(f"Config not found: {args.config}")

    crew, name = load_crew(args.config, user_input)
    print(f"\n=== Running: {name} ===\n")
    result = crew.kickoff()

    out_dir = Path("./outputs") / args.config.stem
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "result.md"
    out_file.write_text(str(result), encoding="utf-8")
    print(f"\nSaved: {out_file}")


if __name__ == "__main__":
    main()
