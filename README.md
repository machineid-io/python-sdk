# MachineID Python SDK

Official Python client for the **MachineID** API.

This SDK provides a thin, explicit wrapper around MachineID’s device enforcement endpoints.  
It is designed for AI agents and distributed systems that need predictable, real-time control over whether a process is allowed to execute.

MachineID acts as an authority layer — not an orchestrator — enabling centralized revoke / allow decisions without managing processes directly.

---

## Installation

pip install machineid-io

---

## Prerequisite (Free Org Key)

MachineID offers a free org key with no billing required.

1. Visit https://machineid.io
2. Create a free organization
3. Copy your org API key (starts with `org_...`)

Set it as an environment variable:

export MACHINEID_ORG_KEY=org_your_key_here

---

## Quick Start

from machineid_io import MachineID

client = MachineID.from_env()
device_id = "agent-01"

# Optional: check plan usage / limits
usage = client.usage()
print("Plan:", usage.get("planTier"), "Limit:", usage.get("limit"))

# Register device (idempotent)
reg = client.register(device_id)

if reg.get("status") not in ("ok", "exists"):
    raise RuntimeError(f"Register failed: {reg}")

print("Register success:", reg.get("status"))

# Validate before performing work (HARD GATE)
val = client.validate(device_id)

if not val.get("allowed"):
    print("Device blocked:", val.get("code"), val.get("request_id"))
    raise SystemExit("Execution denied")

print("Device allowed")

---

## Validate Semantics (Important)

The validate call is the enforcement checkpoint.

- You **must stop execution immediately** when `allowed` is False
- A revoked or blocked device will continue running only if you ignore validate

Validate returns structured decision metadata, including:

- allowed — boolean
- code — stable decision code (ALLOW, DEVICE_REVOKED, PLAN_FROZEN, etc.)
- request_id — correlation ID for logs and support
- status / reason — legacy fields (still included)

---

## Supported Operations

This SDK supports:

- register(device_id)
- validate(device_id)          (POST, canonical)
- list_devices()
- revoke(device_id)
- unrevoke(device_id)
- remove(device_id)
- usage()

All requests authenticate via the `x-org-key` header and return raw API JSON.

---

## Scope

This SDK intentionally does **not**:

- create organizations
- manage billing or checkout
- spawn or orchestrate agents
- perform analytics or metering

It is a device-level enforcement and validation layer only.

---

## Environment-Based Setup

from machineid_io import MachineID

client = MachineID.from_env()

---

## Version

import machineid_io
print(machineid_io.__version__)

---

## Documentation

Docs: https://machineid.io/docs  
Dashboard: https://machineid.io/dashboard  
Pricing: https://machineid.io/pricing

---

## License

MIT
