import uuid
import logging
from datetime import datetime
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("festejo.audit")

class AuditLog:
    def __init__(self):
        self.traces: Dict[str, List[Dict[str, Any]]] = {}

    def log_event(self, execution_id: str, stage: str, status: str, details: Dict[str, Any] = None):
        if execution_id not in self.traces:
            self.traces[execution_id] = []
        
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "stage": stage,
            "status": status,
            "details": details or {}
        }
        self.traces[execution_id].append(entry)
        logger.info(f"[{execution_id}] {stage}: {status}")

audit_log = AuditLog()
