# agents/cve_detection_agent.py
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

# Import tools from centralized registry
from tools import CVE_DETECTION_TOOLS

def create_cve_detection_agent():
    """
    Creates a CVE detection agent with vulnerability database tools.
    """
    return create_react_agent(
        model=ChatOpenAI(model="gpt-4"),
        tools=CVE_DETECTION_TOOLS,
        prompt=(
            "You are a CVE detection specialist. Cross-reference findings with:\n"
            "- NVD 2.0 API for official CVE data\n"
            "- VulnCheck Community API for enhanced information\n"
            "- CVSS scoring for severity assessment\n"
            "- Exploit databases for risk evaluation\n"
            "Provide comprehensive vulnerability context and risk ratings."
        ),
        name="cve_detector"
    )
