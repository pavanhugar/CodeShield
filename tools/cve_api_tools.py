from langchain_core.tools import tool
import requests
import json
import nvdlib
from typing import Optional, Dict, Any
import time


@tool
def nvd_api_searcher(keyword: str, results_per_page: int = 20) -> str:
    """
    Search NIST NVD for CVEs related to keyword.

    Args:
        keyword: Search term for vulnerabilities
        results_per_page: Number of results to return

    Returns:
        JSON string with CVE data
    """
    try:
        base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        params = {
            "keywordSearch": keyword,
            "resultsPerPage": results_per_page
        }

        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()

        return response.text

    except requests.RequestException as e:
        return json.dumps({"error": f"NVD API request failed: {str(e)}"})
    except Exception as e:
        return json.dumps({"error": f"NVD search failed: {str(e)}"})


@tool
def vulncheck_api_client(cve_id: str) -> str:
    """
    Get detailed vulnerability information from VulnCheck API.

    Args:
        cve_id: CVE identifier (e.g., CVE-2023-1234)

    Returns:
        JSON string with vulnerability details
    """
    try:
        # VulnCheck Community API endpoint
        base_url = "https://api.vulncheck.com/v3/index/vulncheck-nvd2"
        params = {"cve": cve_id}

        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()

        return response.text

    except requests.RequestException as e:
        return json.dumps({"error": f"VulnCheck API request failed: {str(e)}"})
    except Exception as e:
        return json.dumps({"error": f"VulnCheck lookup failed: {str(e)}"})


@tool
def cve_severity_assessor(cve_data: str) -> str:
    """
    Assess severity of CVE and provide risk rating.

    Args:
        cve_data: JSON string containing CVE information

    Returns:
        JSON string with severity assessment
    """
    try:
        data = json.loads(cve_data)

        # Extract CVSS scores if available
        cvss_scores = []
        severity_levels = []

        if "vulnerabilities" in data:
            for vuln in data["vulnerabilities"]:
                if "cve" in vuln and "metrics" in vuln["cve"]:
                    metrics = vuln["cve"]["metrics"]

                    # Check for CVSS v3.1 scores
                    if "cvssMetricV31" in metrics:
                        for metric in metrics["cvssMetricV31"]:
                            if "cvssData" in metric:
                                cvss_data = metric["cvssData"]
                                cvss_scores.append(cvss_data.get("baseScore", 0))
                                severity_levels.append(cvss_data.get("baseSeverity", "UNKNOWN"))

        # Calculate risk assessment
        max_score = max(cvss_scores) if cvss_scores else 0
        risk_level = "LOW"

        if max_score >= 9.0:
            risk_level = "CRITICAL"
        elif max_score >= 7.0:
            risk_level = "HIGH"
        elif max_score >= 4.0:
            risk_level = "MEDIUM"
        elif max_score > 0:
            risk_level = "LOW"

        return json.dumps({
            "max_cvss_score": max_score,
            "risk_level": risk_level,
            "severity_levels": severity_levels,
            "total_vulnerabilities": len(cvss_scores),
            "recommendation": get_risk_recommendation(risk_level)
        })

    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid JSON data provided"})
    except Exception as e:
        return json.dumps({"error": f"Severity assessment failed: {str(e)}"})


def get_risk_recommendation(risk_level: str) -> str:
    """Helper function to get recommendations based on risk level."""
    recommendations = {
        "CRITICAL": "Immediate action required. Patch or mitigate immediately.",
        "HIGH": "High priority. Schedule patching within 48 hours.",
        "MEDIUM": "Medium priority. Plan patching within 1 week.",
        "LOW": "Low priority. Include in next maintenance cycle."
    }
    return recommendations.get(risk_level, "Unknown risk level")