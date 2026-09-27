import json
import logging
import os
import re
import sys
import psutil
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def load_config(config_path="config.json"):
    if not os.path.exists(config_path):
        return {
            "cpu_threshold_percent": 80.0,
            "memory_threshold_percent": 85.0,
            "disk_threshold_percent": 90.0,
            "log_file_path": "",
            "log_keywords": ["ERROR", "CRITICAL"],
            "webhook_url": ""
        }
    with open(config_path, "r") as f:
        return json.load(f)

def check_resources(config):
    alerts = []
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    if cpu > config.get("cpu_threshold_percent", 80.0):
        alerts.append(f"HIGH CPU USAGE: {cpu}% exceeds threshold of {config['cpu_threshold_percent']}%")
    if memory > config.get("memory_threshold_percent", 85.0):
        alerts.append(f"HIGH MEMORY USAGE: {memory}% exceeds threshold of {config['memory_threshold_percent']}%")
    if disk > config.get("disk_threshold_percent", 90.0):
        alerts.append(f"HIGH DISK USAGE: {disk}% exceeds threshold of {config['disk_threshold_percent']}%")

    return {"cpu": cpu, "memory": memory, "disk": disk}, alerts

def scan_logs(config):
    alerts = []
    log_path = config.get("log_file_path", "")
    keywords = config.get("log_keywords", ["ERROR", "CRITICAL"])
    
    if log_path and os.path.exists(log_path):
        pattern = re.compile("|".join(keywords), re.IGNORECASE)
        with open(log_path, "r") as f:
            for line in f:
                if pattern.search(line):
                    alerts.append(f"LOG MATCH: {line.strip()}")
    return alerts

def send_alert(webhook_url, message):
    if not webhook_url:
        logging.info("No webhook URL configured. Alert outputted to stdout only.")
        return False
    try:
        response = requests.post(webhook_url, json={"content": message}, timeout=5)
        return response.status_code == 200
    except Exception as e:
        logging.error(f"Failed to send webhook alert: {e}")
        return False

def run_checks():
    config = load_config()
    metrics, resource_alerts = check_resources(config)
    log_alerts = scan_logs(config)
    all_alerts = resource_alerts + log_alerts

    status = "ALERT" if all_alerts else "HEALTHY"
    report = {
        "status": status,
        "metrics": metrics,
        "alerts": all_alerts
    }

    print(json.dumps(report, indent=2))

    if all_alerts and config.get("webhook_url"):
        alert_msg = "\n".join(all_alerts)
        send_alert(config["webhook_url"], f"System Monitor Alert:\n{alert_msg}")

    return report

if __name__ == "__main__":
    run_checks()