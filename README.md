# MachineID Python SDK

Official Python SDK for MachineID.

MachineID is an enforcement control plane — not an orchestrator.  
It provides a hard, authoritative allow / deny decision before code executes.

This SDK is designed for AI agents, workers, schedulers, and distributed systems
that need centralized execution control without managing infrastructure.

---

## Installation

```bash
pip install machineid-io
```

---

## Prerequisite (Free Org Key)

MachineID provides a free organization key with no billing required.

1. Visit https://machineid.io  
2. Create a free organization  
3. Copy your org key (starts with `org_...`)

Set it as an environment variable:

```bash
export MACHINEID_ORG_KEY=org_your_key_here
```

---

## Quick Start (Hard Enforcement)

```python
from machineid import MachineID

m = MachineID.from_env()
device_id = "agent-01"

# Register device (idempotent)
m.register(device_id)

# HARD GATE — MUST stop execution if denied
decision = m.validate(device_id)

if not decision["allowed"]:
    print("Execution denied:", decision["code"], decision["request_id"])
    raise SystemExit(1)

print("Execution allowed")
```

---

## Validate Semantics (Critical)

`validate()` is the enforcement checkpoint.

You must stop execution immediately when:

```python
decision["allowed"] is False
```

Validate returns authoritative decision metadata:

- `allowed` — boolean enforcement decision  
- `code` — stable decision code (e.g. `ALLOW`, `DEVICE_REVOKED`, `PLAN_NOT_ACTIVE`)  
- `request_id` — correlation ID for logs, audits, and support  

Example response:

```json
{
  "allowed": false,
  "code": "DEVICE_REVOKED",
  "request_id": "fbf77ff5-06ed-42eb-8e07-024c32ef1e68"
}
```

---

## System Unavailable (Client Risk Policy)

MachineID enforces **fail-closed execution** by default.

If validation cannot be performed (network failure, timeout, or server error),
execution **must stop**.

For non-critical workloads, the SDK provides an **explicit, opt-in helper** that
allows the client to continue execution **only when the MachineID service is unavailable**.

This is a **client-side risk decision**, not a MachineID guarantee.

Example:

```python
decision = m.validate_or_exit(
    device_id,
    allow_on_system_unavailable=True
)
```

Rules:

- An explicit deny (`allowed == false`) **always stops execution**
- The override only applies when the service cannot be reached
- `validate()` behavior remains unchanged

---

## Supported Operations

This SDK supports:

- `register(device_id)`
- `validate(device_id)` (POST, canonical)
- `validate_or_exit(device_id, ...)` (optional helper)
- `list_devices()`
- `revoke(device_id)`
- `unrevoke(device_id)`
- `remove(device_id)`
- `usage()`

All calls authenticate via the `x-org-key` header  
and return raw API JSON.

---

## Enforcement Rules

- `register()` does NOT restore revoked devices  
- Only `unrevoke()` restores a device  
- `validate()` is POST-only and authoritative  
- Decision codes are stable and intended for programmatic handling  

---

## What This SDK Does NOT Do

This SDK intentionally does NOT:

- create organizations  
- manage billing or checkout  
- orchestrate agents  
- perform analytics or metering  

It is a pure enforcement client.

---

## Environment-Based Setup

```python
from machineid import MachineID

m = MachineID.from_env()
```

---

## Version

```python
import machineid
print(machineid.__version__)
```

---

## Documentation

- Docs: https://machineid.io/docs  
- Dashboard: https://machineid.io/dashboard  
- Pricing: https://machineid.io/pricing  

---

## License

MIT
