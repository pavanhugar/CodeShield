from langchain_core.tools import tool
import git
import os
import tempfile
from github import Github
import json
from typing import Optional


def github_clone_repository(repo_url: str, target_dir: Optional[str] = None) -> str:
    """
    Clone a GitHub repository for analysis.

    Args:
        repo_url: GitHub repository URL
        target_dir: Optional target directory (uses temp if not provided)

    Returns:
        JSON string with clone result and local path
    """
    try:
        if target_dir is None:
            target_dir = os.path.join(os.getcwd(), f"security_scan_{next(tempfile._get_candidate_names())}")
            os.makedirs(target_dir, exist_ok=True)

        # Clone repository
        repo = git.Repo.clone_from(repo_url, target_dir)

        return json.dumps({
            "status": "success",
            "local_path": target_dir,
            "repo_url": repo_url,
            "branch": repo.active_branch.name,
            "commit_hash": str(repo.head.commit)
        })

    except git.GitCommandError as e:
        return json.dumps({"error": f"Git clone failed: {str(e)}"})
    except Exception as e:
        return json.dumps({"error": f"Repository clone failed: {str(e)}"})


@tool
def github_create_branch(repo_path: str, branch_name: str) -> str:
    """
    Create a new branch in the local repository.

    Args:
        repo_path: Path to local git repository
        branch_name: Name for the new branch

    Returns:
        JSON string with branch creation result
    """
    try:
        repo = git.Repo(repo_path)

        # Create new branch
        new_branch = repo.create_head(branch_name)
        new_branch.checkout()

        return json.dumps({
            "status": "success",
            "branch_name": branch_name,
            "commit_hash": str(repo.head.commit)
        })

    except git.GitCommandError as e:
        return json.dumps({"error": f"Branch creation failed: {str(e)}"})
    except Exception as e:
        return json.dumps({"error": f"Branch operation failed: {str(e)}"})

# GitHub integration tools
@tool
def github_api_client(action: str, repo_url: str) -> str:
    """Interact with GitHub API to perform actions."""
    # Implementation would:
    # 1. Authenticate using GitHub token
    # 2. Execute API requests
    # 3. Handle rate limits
    return f"Performed GitHub API action: {action} on {repo_url}"

@tool
def branch_manager(repo_url: str, branch_name: str) -> str:
    """Create and manage branches in the repository."""
    # Implementation would:
    # 1. Clone repository
    # 2. Create new branch
    # 3. Push to remote
    return f"Managed branch: {branch_name} in {repo_url}"

@tool
def pr_documentation_generator(vulnerability_report: str, fixes: str) -> str:
    """Generate documentation for the pull request."""
    # Implementation would:
    # 1. Format vulnerability details
    # 2. Describe applied fixes
    # 3. Include risk assessment
    return f"Generated PR documentation for {len(vulnerability_report.splitlines())} vulnerabilities"

@tool
def security_report_formatter(vulnerability_report: dict) -> str:
    """Format the vulnerability report for the pull request description."""
    # Implementation would:
    # 1. Structure report data
    # 2. Apply markdown formatting
    # 3. Include severity indicators
    return "Formatted security report for PR description"

@tool
def github_create_pull_request(
        repo_url: str,
        title: str,
        body: str,
        head_branch: str,
        base_branch: str = "main",
        github_token: Optional[str] = None
) -> str:
    """
    Create a pull request on GitHub.

    Args:
        repo_url: GitHub repository URL
        title: PR title
        body: PR description
        head_branch: Source branch
        base_branch: Target branch (default: main)
        github_token: GitHub API token

    Returns:
        JSON string with PR creation result
    """
    try:
        if github_token is None:
            github_token = os.getenv("GITHUB_TOKEN")

        if not github_token:
            return json.dumps({"error": "GitHub token not provided"})

        # Extract owner and repo from URL
        parts = repo_url.strip("/").split("/")
        owner = parts[-2]
        repo_name = parts[-1].replace(".git", "")

        # Create GitHub client
        g = Github(github_token)
        repo = g.get_repo(f"{owner}/{repo_name}")

        # Create pull request
        pr = repo.create_pull(
            title=title,
            body=body,
            head=head_branch,
            base=base_branch
        )

        return json.dumps({
            "status": "success",
            "pr_number": pr.number,
            "pr_url": pr.html_url,
            "title": title,
            "head_branch": head_branch,
            "base_branch": base_branch
        })

    except Exception as e:
        return json.dumps({"error": f"PR creation failed: {str(e)}"})
