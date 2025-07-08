# agents/code_scanner_agent.py
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

# Import tools from centralized registry
from tools import CODE_SCANNER_TOOLS

def create_code_scanner_agent():
    """
    Creates a code scanner agent with security analysis tools.
    """
    return create_react_agent(
        model=ChatOpenAI(model="o4-mini"),
        tools=CODE_SCANNER_TOOLS,  # Use pre-defined tool collection
        prompt=(
            "You are a code security scanner. Analyze the code in the file using tools:\n"
            "- AST parsing for structural analysis\n"
            "- Bandit for Python security issues\n"
            "- Semgrep for pattern-based detection\n"
            "- Dependency scanning for known vulnerabilities\n"
            "Provide detailed vulnerability reports with severity assessments."
        ),
        name="code_scanner"
    )