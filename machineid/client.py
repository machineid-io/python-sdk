"""
MachineID Python client

Thin wrapper over the public HTTP API:

- POST /api/v1/devices/register
- POST /api/v1/devices/validate   (canonical)
- GET  /api/v1/devices/list
- POST /api/v1/devices/revoke
- POST /api/v1/devices/unrevoke
- POST /api/v1/devices/remove
- GET  /api/v1/usage

All methods:
- send x-org-key header
- return the parsed JSON response from the API
- do NOT raise on non-2xx; API-level errors come back as JSON
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests


class MachineID:
    def __init__(
        self,
        org_key: str,
        base_url: str = "https://machineid.io",
        timeout: float = 10.0,
    ) -> None:
        if not isinstance(org_key, str) or not org_key.strip():
            raise ValueError("org_key is required")
        self.org_key = org_key.strip()
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    # -----------------------------------------------------------------------
    # Construction helpers
    # -----------------------------------------------------------------------

    @classmethod
    def from_env(
        cls,
        env_var: str = "MACHINEID_ORG_KEY",
        base_url: str = "https://machineid.io",
        timeout: float = 10.0,
    ) -> "MachineID":
        """
        Build a client from an environment variable.

        Example:
          export MACHINEID_ORG_KEY="org_..."
          client = MachineID.from_env()
        """
        value = os.getenv(env_var)
        if not value:
            raise RuntimeError(
                f"Missing {env_var}. Set it in your environment, e.g.\n"
                f"  export {env_var}=org_your_key_here\n"
            )
        return cls(value, base_url=base_url, timeout=timeout)

    # -----------------------------------------------------------------------
    # Internal HTTP helpers
    # -----------------------------------------------------------------------

    def _headers(self, content_type_json: bool = False) -> Dict[str, str]:
        headers: Dict[str, str] = {"x-org-key": self.org_key}
        if content_type_json:
            headers["Content-Type"] = "application/json"
        return headers

    def _parse_response(self, resp: requests.Response) -> Dict[str, Any]:
        try:
            return resp.json()
        except Exception:
            # Keep this simple and explicit; if JSON cannot be parsed, surface it.
            raise RuntimeError(
                f"MachineID API: non-JSON response "
                f"(status={resp.status_code}): {resp.text!r}"
            )

    def _get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        resp = requests.get(
            url,
            headers=self._headers(),
            params=params,
            timeout=self.timeout,
        )
        return self._parse_response(resp)

    def _post(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        resp = requests.post(
            url,
            headers=self._headers(content_type_json=True),
            json=json or {},
            timeout=self.timeout,
        )
        return self._parse_response(resp)

    # -----------------------------------------------------------------------
    # Public methods (device lifecycle + usage)
    # -----------------------------------------------------------------------

    def register(self, device_id: str) -> Dict[str, Any]:
        """
        POST /api/v1/devices/register
        Body: { "deviceId": "<string>" }
        """
        if not isinstance(device_id, str) or not device_id.strip():
            raise ValueError("device_id is required")
        payload = {"deviceId": device_id.strip()}
        return self._post("/api/v1/devices/register", json=payload)

    def validate(self, device_id: str) -> Dict[str, Any]:
        """
        POST /api/v1/devices/validate  (canonical)
        Body: { "deviceId": "<string>" }

        Returns API JSON including:
        - allowed: bool
        - code: decision code (e.g., ALLOW, DEVICE_REVOKED, PLAN_FROZEN, ...)
        - request_id: correlation id
        """
        if not isinstance(device_id, str) or not device_id.strip():
            raise ValueError("device_id is required")
        payload = {"deviceId": device_id.strip()}
        return self._post("/api/v1/devices/validate", json=payload)

    def list_devices(self) -> Dict[str, Any]:
        """
        GET /api/v1/devices/list
        """
        return self._get("/api/v1/devices/list")

    def revoke(self, device_id: str) -> Dict[str, Any]:
        """
        POST /api/v1/devices/revoke
        Body: { "deviceId": "<string>" }
        """
        if not isinstance(device_id, str) or not device_id.strip():
            raise ValueError("device_id is required")
        payload = {"deviceId": device_id.strip()}
        return self._post("/api/v1/devices/revoke", json=payload)

    def unrevoke(self, device_id: str) -> Dict[str, Any]:
        """
        POST /api/v1/devices/unrevoke
        Body: { "deviceId": "<string>" }
        """
        if not isinstance(device_id, str) or not device_id.strip():
            raise ValueError("device_id is required")
        payload = {"deviceId": device_id.strip()}
        return self._post("/api/v1/devices/unrevoke", json=payload)

    # Optional alias if you want a friendlier name in templates.
    restore = unrevoke

    def remove(self, device_id: str) -> Dict[str, Any]:
        """
        POST /api/v1/devices/remove
        Body: { "deviceId": "<string>" }

        Hard-delete a device for this org.
        """
        if not isinstance(device_id, str) or not device_id.strip():
            raise ValueError("device_id is required")
        payload = {"deviceId": device_id.strip()}
        return self._post("/api/v1/devices/remove", json=payload)

    def usage(self) -> Dict[str, Any]:
        """
        GET /api/v1/usage
        """
        return self._get("/api/v1/usage")
