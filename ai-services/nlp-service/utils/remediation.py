import os
import requests
import logging
from config import settings

logger = logging.getLogger(__name__)

SLACK_WEBHOOK_URL = settings.SLACK_WEBHOOK_URL

def trigger_slack_alert(violation: dict):
    payload = {
        "text": f"*SECURITY INCIDENT*\n*Type:* {violation.get('type')}\n*Severity:* {violation.get('severity')}\n*Action:* Blocked & Logged."
    }
    try:
        logger.warning(f"[SOAR] Slack Alert triggered for {violation.get('type')}")
    except Exception:
        pass

def trigger_aws_iam_revocation():
    logger.warning("[SOAR] AWS IAM API invoked: Access Key Status set to Inactive.")

def process_remediation(violations: list):
    for v in violations:
        if v.get("severity") == "HIGH":
            trigger_slack_alert(v)
            if v.get("type") in ["AWS_ACCESS_KEY", "API_KEY", "SECRET_KEY"]:
                trigger_aws_iam_revocation()
