# MachineID.io Python SDK

Official Python client for the **MachineID.io** API.

This SDK provides a thin, explicit wrapper around MachineID’s device and usage endpoints. It is designed for AI agents and distributed systems that need predictable device-level control.

---

## Installation

```bash
pip install machineid-io
```

---

## Prerequisite

Create a free org and generate an org key at:

https://machineid.io

Set it as an environment variable:

```bash
export MACHINEID_ORG_KEY=org_your_key_here
```

---

## Quick Start

```python
from machineid_io import MachineID

client = MachineID.from_env()
device_id = "agent-01"

# Check usage / plan limits
usage = client.usage()
print("Plan:", usage["planTier"], "Limit:", usage["limit"])

# Register device (idempotent)
reg = client.register(device_id)
print("Register status:", reg["status"])

# Validate before performing work
val = client.validate(device_id)
if not val.get("allowed"):
    raise SystemExit("Device blocked")

print("Device allowed:", val.get("reason"))
```

---

## Supported Operations

This SDK supports:

- `register(device_id)`
- `validate(device_id)`
- `list_devices()`
- `revoke(device_id)`
- `unrevoke(device_id)`
- `remove(device_id)`
- `usage()`

All requests authenticate via the `x-org-key` header and return raw API JSON.

---

## Scope

This SDK intentionally does **not**:

- create orgs
- manage billing or checkout
- spawn or orchestrate agents
- perform analytics or metering

It is a device-level validation and control layer only.

---

## Environment-Based Setup

```python
from machineid_io import MachineID

client = MachineID.from_env()
```

---

## Version

```python
import machineid_io
print(machineid_io.__version__)
```

---

## Documentation

- API reference: https://machineid.io/api
- Docs: https://machineid.io/docs

---

## License

MIT
