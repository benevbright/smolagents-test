import os
import sys
from smolagents import CodeAgent, ApiWebSearchTool, OpenAIServerModel, tool
from dotenv import load_dotenv
import subprocess

load_dotenv()

@tool
def execute_bash(command: str, timeout: int = 10) -> str:
    """
    Executes a bash command on the local machine and returns its output.

    Args:
        command: The full command string to run in the terminal (e.g., 'ls -la', 'pwd').
        timeout: The maximum execution time in seconds.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode == 0:
            return result.stdout if result.stdout else "Command executed successfully with no output."
        else:
            return f"Error (Exit Code {result.returncode}): {result.stderr}"
    except Exception as e:
        return f"Execution failed: {str(e)}"
    
def main():
    if len(sys.argv) < 2:
        print("add prompt")
        return
    
    user_query = sys.argv[1]

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
        tools=[execute_bash, brave_tool],
        model=model,
        stream_outputs=True,
        additional_authorized_imports=["*"]
    )

    agent.run(user_query)