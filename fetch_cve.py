import requests
from elasticsearch import Elasticsearch
from datetime import datetime, timezone

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

def fetch_cves():
    print("Fetching CVE data from NVD...")
    
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    params = {
        "resultsPerPage": 20,
        "startIndex": 0,
        "cvssV3Severity": "CRITICAL"  # Only fetch CRITICAL vulnerabilities
    }
    
    response = requests.get(url, params=params, timeout=30)
    data = response.json()
    
    cves = data.get("vulnerabilities", [])
    print(f"Found {len(cves)} critical CVEs")
    
    for item in cves:
        cve = item.get("cve", {})
        cve_id = cve.get("id", "Unknown")
        published = cve.get("published", "")
        description = cve.get("descriptions", [{}])[0].get("value", "No description")
        
        # Get CVSS score if available
        score = None
        try:
            score = cve["metrics"]["cvssMetricV31"][0]["cvssData"]["baseScore"]
        except (KeyError, IndexError):
            score = 0.0
        
        # Build document to send to Elasticsearch
        doc = {
            "cve_id": cve_id,
            "published": published,
            "description": description,
            "severity": "CRITICAL",
            "score": score,
            "indexed_at": datetime.now(timezone.utc).isoformat()
        }
        
        # Push to Elasticsearch
        es.index(index="cve-alerts", document=doc)
        print(f"Indexed: {cve_id} | Score: {score}")

    print("\nDone! All CVEs pushed to Elasticsearch.")

if __name__ == "__main__":
    fetch_cves()