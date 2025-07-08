# agents/supervisor_agent.py
from langgraph_supervisor import create_supervisor
from langchain_openai import ChatOpenAI
from typing import List, Callable


def create_supervisor_agent(agent_creators: List[Callable]):
    """
    Creates supervisor agent that coordinates other agents.

    Args:
        agent_creators: List of agent creation functions
    """
    # Create agents from the provided creation functions
    agents = [creator() for creator in agent_creators]

    return create_supervisor(
        agents=agents,
        model=ChatOpenAI(model="o4-mini"),
        prompt=(
            f"You are a security analysis supervisor managing {len(agents)} specialized agents:\n"
            #"The input to this supervisor is a text containing code after cloning the github repo to local directory\n"
            "The input text will in following format:\n"
            "# File: <python file name>\n "
            #"content of the file\n \n \n again # File: <python file name>\n content of the file\n \n \n\n"
            #"your job is to parse the input text and for each file name followed by code"
            " 1) you do not need to read the files and parse the code, you will get the file names which has the code"
            " 2) pass the file as an input to agents which parse the ode to identify security vulnerabilities"
            " 3) provide the details of number security vulnerabilities identified if any like CVE and description"
            " 4)where in the code has the vulnerability 5) suggest the code fix to remediate the issue\n"
            "use the following agents depending on the task you need to perform\n"
            "- Code Scanner: Analyzes code for vulnerabilities\n"
            "- CVE Detector: Cross-references findings with vulnerability databases\n"
            #"- Fix Generator: Creates code fixes and security improvements\n"
            #"- PR Creator: Manages pull request creation and documentation\n"
            "Coordinate tasks sequentially and ensure comprehensive analysis. Provide detailed reports and actionable insights before each call to agent with reasons\n"
            "if there are no vulnerabilities found in the code, then you need to return a message saying no vulnerabilities found in the code\n"
        ),
        add_handoff_back_messages=True,
        output_mode="full_history"
    )