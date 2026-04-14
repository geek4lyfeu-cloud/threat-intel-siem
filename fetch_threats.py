import requests
from elasticsearch import Elasticsearch
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================
# CONFIG
# ============================================
ABUSEIPDB_KEY = os.getenv("ABUSEIPDB_KEY")
OTX_KEY = os.getenv("OTX_KEY")

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# ============================================
# SOURCE 1 — AbuseIPDB (Malicious IPs)
# ============================================
def fetch_malicious_ips():
    print("\n🔍 Fetching malicious IPs from AbuseIPDB...")
    
    url = "https://api.abuseipdb.com/api/v2/blacklist"
    headers = {
        "Key": ABUSEIPDB_KEY,
        "Accept": "application/json"
    }
    params = {
        "confidenceMinimum": 90,
        "limit": 20
    }
    
    response = requests.get(url, headers=headers, params=params, timeout=30)
    data = response.json()
    
    ips = data.get("data", [])
    print(f"Found {len(ips)} malicious IPs")
    
    for ip in ips:
        doc = {
            "alert_type": "Malicious IP",
            "severity": "HIGH",
            "score": 7.5,
            "ip_address": ip.get("ipAddress"),
            "abuse_confidence": ip.get("abuseConfidenceScore"),
            "country": ip.get("countryCode"),
            "total_reports": ip.get("totalReports"),
            "description": f"Malicious IP {ip.get('ipAddress')} reported {ip.get('totalReports')} times",
            "indexed_at": datetime.now(timezone.utc).isoformat()
        }
        
        es.index(index="threat-alerts", document=doc)
        print(f"Indexed: {ip.get('ipAddress')} | Country: {ip.get('countryCode')} | Reports: {ip.get('totalReports')}")

# ============================================
# SOURCE 2 — AlienVault OTX (Threat Intel)
# ============================================
def fetch_otx_threats():
    print("\n🔍 Fetching threat intelligence from AlienVault OTX...")
    
    url = "https://otx.alienvault.com/api/v1/pulses/subscribed"
    headers = {
        "X-OTX-API-KEY": OTX_KEY
    }
    params = {
        "limit": 10
    }
    
    response = requests.get(url, headers=headers, params=params, timeout=30)
    data = response.json()
    
    pulses = data.get("results", [])
    print(f"Found {len(pulses)} threat pulses")
    
    for pulse in pulses:
        # Determine severity based on TLP
        tlp = pulse.get("tlp", "white").lower()
        if tlp == "red":
            severity = "CRITICAL"
            score = 9.0
        elif tlp == "amber":
            severity = "HIGH"
            score = 7.0
        else:
            severity = "MEDIUM"
            score = 5.0
        
        doc = {
            "alert_type": "Threat Intelligence",
            "severity": severity,
            "score": score,
            "pulse_name": pulse.get("name"),
            "author": pulse.get("author_name"),
            "tags": ", ".join(pulse.get("tags", [])),
            "indicator_count": pulse.get("indicator_count", 0),
            "description": pulse.get("description") or pulse.get("name"),
            "indexed_at": datetime.now(timezone.utc).isoformat()
        }
        
        es.index(index="threat-alerts", document=doc)
        print(f"Indexed: {pulse.get('name')} | Severity: {severity} | Indicators: {pulse.get('indicator_count')}")

# ============================================
# RUN ALL
# ============================================
if __name__ == "__main__":
    fetch_malicious_ips()
    fetch_otx_threats()
    print("\n✅ Done! All threats pushed to Elasticsearch.")