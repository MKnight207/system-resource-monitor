import os
import json
import pytest
from src.monitor import load_config, check_resources, scan_logs

def test_load_config_default(tmp_path):
    non_existent = tmp_path / "no_config.json"
    config = load_config(str(non_existent))
    assert config["cpu_threshold_percent"] == 80.0

def test_check_resources_trigger_alerts():
    config = {
        "cpu_threshold_percent": 0.0,
        "memory_threshold_percent": 0.0,
        "disk_threshold_percent": 0.0
    }
    metrics, alerts = check_resources(config)
    assert len(alerts) == 3

def test_scan_logs_regex(tmp_path):
    log_file = tmp_path / "test.log"
    log_file.write_text("INFO: System normal\nERROR: Disk drive failure\nCRITICAL: Power loss\n")
    
    config = {
        "log_file_path": str(log_file),
        "log_keywords": ["ERROR", "CRITICAL"]
    }
    
    alerts = scan_logs(config)
    assert len(alerts) == 2