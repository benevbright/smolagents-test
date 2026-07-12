import os
import sys
from pathlib import Path

from agent.sat import start_agent_bot
from agent.tools import bash_tool
from smolagents import CodeAgent, ApiWebSearchTool, OpenAIServerModel
from dotenv import load_dotenv

load_dotenv()

def generate_client(on_message, user_id):
    """
    Creates a CodeAgent configured to use the provided on_message tool for replies.
    """

    project_root = Path(__file__).resolve().parents[2]
    system_md_path = project_root / "SYSTEM.md"
    system_prompt = system_md_path.read_text().strip() if system_md_path.exists() else ""

    model_id = os.getenv("MODEL_ID")
    llm_api_base = os.getenv("LLM_API_BASE")
    llm_api_key = os.getenv("LLM_API_KEY")
    if not model_id:
        raise ValueError("MODEL_ID is not set")

    model = OpenAIServerModel(
        model_id=model_id,
        api_base=llm_api_base,
        api_key=llm_api_key,
    )

    brave_api_key = os.getenv("BRAVE_API_KEY")
    if not brave_api_key:
        raise ValueError("BRAVE_API_KEY is not set")
    brave_tool = ApiWebSearchTool(api_key=brave_api_key)

    agent = CodeAgent(
        tools=[bash_tool, brave_tool, on_message],
        model=model,
        stream_outputs=True,
        additional_authorized_imports=["*"],
        instructions=system_prompt
    )
    return agent

def main():
    telegram_token = os.environ.get("TELEGRAM_TOKEN")
    if not telegram_token:
        raise ValueError("TELEGRAM_TOKEN not found. Did you create a .env file?")

    print("Starting Telegram bot...")
    start_agent_bot(
        telegram_token=telegram_token,
        generate_agent_fn=generate_client
    )