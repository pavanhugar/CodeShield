# main.py
"""
Main orchestration script for multi-agent security vulnerability scanner.
"""
import json
import os
from dotenv import load_dotenv
from tools import github_clone_repository
from pathlib import Path
# Load environment variables
load_dotenv()

# Import agent creation functions (no circular dependency)
from Agents.supervisor_agent import create_supervisor_agent
from Agents.code_scanner_agent import create_code_scanner_agent
from Agents.cve_detection_agent import create_cve_detection_agent
from Agents.fix_generator_agent import create_fix_generator_agent
from Agents.pr_creator_agent import create_pr_creator_agent


def main():
    """
    Main function to run the security vulnerability scanner.
    """
    # List of agent creation functions (not instances)
    agent_creators = [
        create_code_scanner_agent,
        create_cve_detection_agent,
        create_fix_generator_agent,
        create_pr_creator_agent
    ]

    # Create supervisor with agent creators
    supervisor = create_supervisor_agent(agent_creators)

    # Compile the workflow
    app = supervisor.compile()

    # Example usage
    github_url = input("Enter GitHub repository URL: ")
    if not github_url:
        print("No repository URL provided. Exiting.")
        return
    github_token = os.getenv("GITHUB_TOKEN")
    url = f"https://{github_token}@github.com/pavanhugar/office-hour-assistant.git"
    repo_path = github_clone_repository(url)
    repo_info=json.loads(repo_path)
    scan_path=repo_info.get("local_path", "No local path found.")
    print(scan_path)
    all_text = ""
    print(Path(scan_path).glob("*.py"))
    for file in Path(scan_path).glob("*.py"):
        print(f"Reading file: {scan_path}/{file.name}")
        with (open(file, "r", encoding="utf-8") as f):
            all_text += f"# File: {scan_path}/{file.name}\n"
            #+ f.read()
    print(all_text)
    print("Starting security scan...")

    result = app.invoke({
        "messages": [{
            "role": "user",
            "content": f"Scan these files for security vulnerabilities: {all_text}"
        }]
    })

    print("Security scan completed!")
    print(result)


if __name__ == "__main__":
    main()