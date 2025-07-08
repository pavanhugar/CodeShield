# tools/__init__.py
"""
Centralized tool registry for multi-agent security scanner.
Import all tools here to avoid circular dependencies.
"""

# Code analysis tools
from .code_analysis_tools import (
    ast_vulnerability_scanner,
    bandit_security_analyzer,
    semgrep_pattern_matcher,
    dependency_vulnerability_checker
)

# CVE detection tools
from .cve_api_tools import (
    nvd_api_searcher,
    vulncheck_api_client,
    cve_severity_assessor
)

# Security fix tools
from .security_tools import (
    security_pattern_applier,
    code_fix_generator,
    vulnerability_remediation_advisor,
    security_best_practices_checker
)

# GitHub integration tools
from .github_tools import (
    github_clone_repository,
    github_create_branch,
    github_create_pull_request,
    github_api_client,
    branch_manager,
    pr_documentation_generator,
    security_report_formatter
)

# Tool collections by agent type
CODE_SCANNER_TOOLS = [
    ast_vulnerability_scanner,
    bandit_security_analyzer,
    semgrep_pattern_matcher,
    dependency_vulnerability_checker
]

CVE_DETECTION_TOOLS = [
    nvd_api_searcher,
    vulncheck_api_client,
    cve_severity_assessor
    #exploit_information_gatherer
]

FIX_GENERATOR_TOOLS = [
    security_pattern_applier,
    code_fix_generator,
    vulnerability_remediation_advisor,
    security_best_practices_checker
]

PR_CREATOR_TOOLS = [
    github_clone_repository,
    github_create_branch,
    github_create_pull_request,
    github_api_client,
    branch_manager,
    pr_documentation_generator,
    security_report_formatter
]

# Export all tools
__all__ = [
    # Individual tools
    "ast_vulnerability_scanner",
    "bandit_security_analyzer",
    "semgrep_pattern_matcher",
    "dependency_vulnerability_checker",
    "nvd_api_searcher",
    "vulncheck_api_client",
    "cve_severity_assessor",
    #"exploit_information_gatherer",
    "security_pattern_applier",
    "code_fix_generator",
    "vulnerability_remediation_advisor",
    "security_best_practices_checker",
    "github_clone_repository",
    "github_create_branch",
    "github_create_pull_request",
    "github_api_client",
    "branch_manager",
    "pr_documentation_generator",
    "security_report_formatter",

    # Tool collections
    "CODE_SCANNER_TOOLS",
    "CVE_DETECTION_TOOLS",
    "FIX_GENERATOR_TOOLS",
    "PR_CREATOR_TOOLS"
]