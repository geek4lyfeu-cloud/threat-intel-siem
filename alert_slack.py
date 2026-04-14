import requests
from elasticsearch import Elasticsearch
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

load_dotenv()


# ============================================
# CONFIG
# ============================================
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# ============================================
# FETCH HIGH/CRITICAL ALERTS FROM ES
# ============================================
def fetch_critical_alerts():
    print("🔍 Checking for critical alerts...")
    
    query = {
        "query": {
            "terms": {
                "severity.keyword": ["CRITICAL", "HIGH"]
            }
        },
        "sort": [{"indexed_at": {"order": "desc"}}],
        "size": 3
    }
    
    response = es.search(index="threat-alerts", body=query)
    hits = response["hits"]["hits"]
    
    print(f"Found {len(hits)} critical/high alerts")
    return hits

# ============================================
# SEND ALERT TO SLACK
# ============================================
def send_slack_alert(alert):
    source = alert["_source"]
    
    severity = source.get("severity", "UNKNOWN")
    alert_type = source.get("alert_type", "Unknown")
    description = source.get("description", "No description")
    score = source.get("score", 0)
    country = source.get("country", "Unknown")
    indexed_at = source.get("indexed_at", "")
    
    # Emoji based on severity
    if severity == "CRITICAL":
        emoji = "🔴"
    elif severity == "HIGH":
        emoji = "🟠"
    else:
        emoji = "🟡"
    
    message = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{emoji} {severity} THREAT DETECTED"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Alert Type:*\n{alert_type}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Severity:*\n{severity}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Score:*\n{score}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Country:*\n{country}"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Description:*\n{description}"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"🕐 Detected at: {indexed_at}"
                    }
                ]
            },
            {
                "type": "divider"
            }
        ]
    }
    
    response = requests.post(SLACK_WEBHOOK, json=message)
    
    if response.status_code == 200:
        print(f"✅ Alert sent to Slack: {alert_type} | {severity}")
    else:
        print(f"❌ Failed to send: {response.status_code}")

# ============================================
# RUN
# ============================================
if __name__ == "__main__":
    alerts = fetch_critical_alerts()
    
    if not alerts:
        print("✅ No critical alerts found.")
    else:
        print(f"\n📤 Sending {len(alerts)} alerts to Slack...\n")
        for alert in alerts:
            send_slack_alert(alert)
    
    print("\n✅ Done!")