from langchain_core.tools import tool
import ast
import subprocess
import json
import os
from typing import Dict, Any


@tool
def ast_vulnerability_scanner(file_path: str) -> str:
    """
    Scan Python file for AST-level security vulnerabilities.

    Args:
        file_path: Path to the Python file to scan

    Returns:
        JSON string with vulnerability findings
    """
    try:
        with open(file_path, 'r') as f:
            source_code = f.read()

        tree = ast.parse(source_code)
        vulnerabilities = []

        # Check for common security issues
        for node in ast.walk(tree):
            # Check for exec() usage
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == 'exec':
                    vulnerabilities.append({
                        "type": "dangerous_function",
                        "function": "exec",
                        "line": node.lineno,
                        "severity": "HIGH",
                        "description": "Use of exec() can lead to code injection"
                    })

                # Check for eval() usage
                elif isinstance(node.func, ast.Name) and node.func.id == 'eval':
                    vulnerabilities.append({
                        "type": "dangerous_function",
                        "function": "eval",
                        "line": node.lineno,
                        "severity": "HIGH",
                        "description": "Use of eval() can lead to code injection"
                    })

        return json.dumps({
            "file": file_path,
            "vulnerabilities": vulnerabilities,
            "total_issues": len(vulnerabilities)
        })

    except Exception as e:
        return f"Error scanning file {file_path}: {str(e)}"


@tool
def bandit_security_analyzer(directory_path: str) -> str:
    """
    Run Bandit security analysis on a directory.

    Args:
        directory_path: Path to directory to scan

    Returns:
        JSON string with Bandit findings
    """
    try:
        # Run bandit command
        result = subprocess.run(
            ['bandit', '-r', directory_path, '-f', 'json'],
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode == 0:
            return result.stdout
        else:
            # Bandit returns non-zero when vulnerabilities found
            return result.stdout if result.stdout else result.stderr

    except subprocess.TimeoutExpired:
        return json.dumps({"error": "Bandit scan timed out"})
    except Exception as e:
        return json.dumps({"error": f"Bandit scan failed: {str(e)}"})


@tool
def semgrep_pattern_matcher(directory_path: str, rules: str = "auto") -> str:
    """
    Run Semgrep pattern matching on directory.

    Args:
        directory_path: Path to directory to scan
        rules: Semgrep rules to use (default: auto)

    Returns:
        JSON string with Semgrep findings
    """
    try:
        cmd = ['semgrep', '--config', rules, '--json', directory_path]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )

        return result.stdout if result.stdout else result.stderr

    except subprocess.TimeoutExpired:
        return json.dumps({"error": "Semgrep scan timed out"})
    except Exception as e:
        return json.dumps({"error": f"Semgrep scan failed: {str(e)}"})


@tool
def dependency_vulnerability_checker(requirements_file: str) -> str:
    """
    Check dependencies for known vulnerabilities using safety.

    Args:
        requirements_file: Path to requirements.txt or similar file

    Returns:
        JSON string with vulnerability findings
    """
    try:
        result = subprocess.run(
            ['safety', 'check', '-r', requirements_file, '--json'],
            capture_output=True,
            text=True,
            timeout=120
        )

        return result.stdout if result.stdout else result.stderr

    except subprocess.TimeoutExpired:
        return json.dumps({"error": "Safety check timed out"})
    except Exception as e:
        return json.dumps({"error": f"Safety check failed: {str(e)}"})