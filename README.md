# 🛡️ Automated Threat Intelligence SIEM Pipeline
A real-time Security Information and Event Management (SIEM) pipeline that aggregates threat intelligence from multiple sources, visualizes security events in Kibana, and sends automated alerts to Slack.

## 📌 Project Overview
This project simulates a real-world SOC(Security Operations Center) monitoring pipeline built entirely with free, industry-standard tools.

## 🔧 Tech Stack
| Tool | Purpose |
|---|---|
| Python | Data fetching & automation |
| Elasticsearch + Kibana | Storage & dashboard visualization |
| Docker | Container orchestration |
| NVD API | Real CVE vulnerability data |
| AbuseIPDB API | Real malicious IP intelligence |
| AlienVault OTX | Real threat intelligence feeds |
| Slack Webhook | Automated daily alerting |

## 🚀 How to Run

### Prerequisites
- Docker Desktop
- Python 3.x
- Free API keys for AbuseIPDB, AlienVault OTX
- Slack Webhook URL

### Setup
1. Clone the repository
```bash
git clone https://github.com/geek4lyfeu-cloud/threat-intel-siem.git
cd threat-intel-siem
```
2. Start ELK Stack
```bash
docker-compose up -d
```
3. Install Python dependencies
```bash
pip install -r requirements.txt
```
4. Create `.env` file with your API keys
ABUSEIPDB_KEY=your_key_here
OTX_KEY=your_key_here
SLACK_WEBHOOK=your_webhook_here

5. Run the pipeline
```bash
python scheduler.py
```
6. Open Kibana dashboard
http://localhost:5601

## 📱 Slack Alerts

Automated alerts are sent to the `#threat-alerts` Slack channel daily at 08:00 AM, including:
- 🔴 CRITICAL threats
- 🟠 HIGH severity malicious IPs
- Real IP addresses, countries, and threat descriptions

## 🔑 API Keys Required

- [NVD API](https://nvd.nist.gov/) — Free
- [AbuseIPDB](https://www.abuseipdb.com/register) — Free (1000 calls/day)
- [AlienVault OTX](https://otx.alienvault.com) — Free
- Slack Incoming Webhook — Free

## ⚠️ Disclaimer

This project is for educational purposes only. All threat data is sourced from public APIs.
