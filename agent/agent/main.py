import os
import sys
from pathlib import Path

from agent.tools import bash_tool
from smolagents import CodeAgent, ApiWebSearchTool, OpenAIServerModel
from dotenv import load_dotenv

load_dotenv()
    
def main():
    if len(sys.argv) < 2:
        print("add prompt")
        return
    
    user_query = sys.argv[1]

    project_root = Path(__file__).resolve().parents[2]
    system_md_path = project_root / "SYSTEM.md"
    system_prompt = system_md_path.read_text().strip() if system_md_path.exists() else ""

    model = OpenAIServerModel(
        model_id="custom/localllm",
        api_base="http://localhost:8090/v1",
        api_key="dummy",
    )

    brave_api_key = os.getenv("BRAVE_API_KEY")
    if not brave_api_key:
        raise ValueError("BRAVE_API_KEY is not set")
    brave_tool = ApiWebSearchTool(api_key=brave_api_key)

    agent = CodeAgent(
        tools=[bash_tool, brave_tool],
        model=model,
        stream_outputs=True,
        additional_authorized_imports=["*"],
        instructions=system_prompt
    )

    agent.run(user_query)