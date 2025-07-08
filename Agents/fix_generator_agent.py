from langgraph.prebuilt import create_react_agent

from tools import FIX_GENERATOR_TOOLS
def create_fix_generator_agent():
    tools = FIX_GENERATOR_TOOLS

    return create_react_agent(
        model="openai:gpt-4",
        tools=tools,
        prompt=(
            "You are a security fix generator. Create code improvements that:"
            "- Address identified vulnerabilities effectively"
            "- Follow security best practices and standards"
            "- Maintain code functionality and performance"
            "- Include clear explanations and documentation"
            "Generate production-ready security fixes with comprehensive explanations."
        ),
        name="fix_generator"
    )