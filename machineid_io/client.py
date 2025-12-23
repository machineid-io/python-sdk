# machineid_io/client.py
"""
MachineID Python SDK

Endpoints:
- POST /api/v1/devices/register
- POST /api/v1/devices/validate  (canonical)
- GET  /api/v1/devices/list
- POST /api/v1/devices/revoke
- POST /api/v1/devices/unrevoke
- POST /api/v1/devices/revoke_batch
- POST /api/v1/devices/unrevoke_batch
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass
class ValidateResult:
    allowed: bool
    code: Optional[str] = None
    request_id: Optional[str] = None
    status: Optional[str] = None
    reason: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None


class MachineIDClient:
    def __init__(self, org_key: str, base_url: str = "https://machineid.io", timeout: int = 15):
        self.org_key = org_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "x-org-key": self.org_key,
        }

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        r = requests.get(url, headers=self._headers(), params=params, timeout=self.timeout)
        # Return JSON even on non-2xx (caller may want error fields)
        return r.json()

    def _post(self, path: str, body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        r = requests.post(url, headers=self._headers(), json=(body or {}), timeout=self.timeout)
        return r.json()

    # -----------------------
    # Core endpoints
    # -----------------------

    def register(self, device_id: str) -> Dict[str, Any]:
        return self._post("/api/v1/devices/register", {"deviceId": device_id})

    def validate(self, device_id: str) -> ValidateResult:
        """
        Canonical validate (POST).
        Returns ValidateResult with:
          - allowed (bool)
          - code (str) e.g. ALLOW, DEVICE_REVOKED, PLAN_FROZEN, ...
          - request_id (str) correlation id
        """
        d = self._post("/api/v1/devices/validate", {"deviceId": device_id})

        allowed = bool(d.get("allowed", False))
        return ValidateResult(
            allowed=allowed,
            code=d.get("code"),
            request_id=d.get("request_id"),
            status=d.get("status"),
            reason=d.get("reason"),
            raw=d,
        )

    def list_devices(self) -> Dict[str, Any]:
        return self._get("/api/v1/devices/list")

    def revoke(self, device_id: str) -> Dict[str, Any]:
        return self._post("/api/v1/devices/revoke", {"deviceId": device_id})

    def unrevoke(self, device_id: str) -> Dict[str, Any]:
        return self._post("/api/v1/devices/unrevoke", {"deviceId": device_id})
