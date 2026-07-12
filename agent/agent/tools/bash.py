import os

from smolagents import tool
import subprocess

@tool
def bash_tool(command: str, timeout: int = 10) -> str:
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
            timeout=timeout,
            env=os.environ
        )
        if result.returncode == 0:
            return result.stdout if result.stdout else "Command executed successfully with no output."
        else:
            return f"Error (Exit Code {result.returncode}): {result.stderr}"
    except Exception as e:
        return f"Execution failed: {str(e)}"
    