import schedule
import time
import subprocess
from datetime import datetime, timezone

def run_daily_threat_fetch():
    print(f"\n⏰ Daily threat fetch started at {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC")
    
    # Step 1 — Fetch CVEs
    print("\n📡 Step 1: Fetching CVEs from NVD...")
    subprocess.run(["python", "fetch_cve.py"])
    
    # Step 2 — Fetch Threats (AbuseIPDB + OTX)
    print("\n📡 Step 2: Fetching threats from AbuseIPDB + AlienVault OTX...")
    subprocess.run(["python", "fetch_threats.py"])
    
    # Step 3 — Send top alerts to Slack
    print("\n📤 Step 3: Sending critical alerts to Slack...")
    subprocess.run(["python", "alert_slack.py"])
    
    print(f"\n✅ Daily threat fetch complete!")

# ============================================
# SCHEDULE — runs once daily at 8:00 AM
# ============================================
schedule.every().day.at("08:00").do(run_daily_threat_fetch)

print("🚀 SIEM Scheduler started!")
print("⏰ Daily threat fetch scheduled at 08:00 AM")
print("💡 Press Ctrl+C to stop\n")

# Run immediately on start so you can test it
print("▶️ Running initial fetch now...")
run_daily_threat_fetch()

# Keep running
while True:
    schedule.run_pending()
    time.sleep(60)