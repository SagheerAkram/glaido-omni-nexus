"""
Base Tool Contract
Defines the abstract base class and type protocols for all Glaido Omni-Nexus core tools.
"""

from typing import Dict, Any, Optional
import time
from datetime import datetime, timezone

class CoreVerificationTool:
    """Base class defining the strict JSON contract for all verification tools."""
    
    TOOL_CATEGORY: str = "unknown"
    
    def run_check(self) -> Dict[str, Any]:
        """Execute tool logic and return standardized report."""
        start_time = time.time()
        
        try:
            status, results, message, actionable, remediation = self._execute_impl()
        except Exception as e:
            status, results, message, actionable, remediation = "error", {"error": str(e)}, "Unhandled tool exception", True, "Inspect tool implementation."
            
        return {
            "category": self.TOOL_CATEGORY,
            "status": status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": message,
            "actionable": actionable,
            "remediation": remediation,
            "results": results,
            "metrics": {
                "duration_ms": round((time.time() - start_time) * 1000, 2)
            }
        }
        
    def _execute_impl(self) -> tuple[str, dict, str, bool, Optional[str]]:
        """
        Implementation logic to be overridden.
        Returns: (status, results_dict, message, actionable, remediation)
        """
        raise NotImplementedError("Tool must implement _execute_impl")
