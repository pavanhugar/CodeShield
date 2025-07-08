from langgraph.prebuilt import create_react_agent
from tools import PR_CREATOR_TOOLS
def create_pr_creator_agent():
    tools = PR_CREATOR_TOOLS

    return create_react_agent(
        model="openai:gpt-4",
        tools=tools,
        prompt=(
            "You are a PR creation specialist. Manage repository integration by:"
            "- Creating feature branches for security fixes"
            "- Generating comprehensive pull requests"
            "- Including detailed security documentation"
            "- Facilitating code review and approval processes"
            "Create professional PRs with complete security context."
        ),
        name="pr_creator"
    )