# System Resource & Log Alerting Tool

A lightweight Python and Bash system health monitoring utility that tracks CPU, RAM, and disk utilization, parses system logs for critical error patterns, and dispatches alerts via external webhooks.

## Features
* **System Metric Tracking:** Monitors CPU, memory, and disk health (`psutil`).
* **Log Regex Engine:** Scans log files for configurable incident patterns.
* **Automated CI/CD:** Integrated test execution using `pytest` and GitHub Actions.

## Setup & Execution
```powershell
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
python -m src.monitor