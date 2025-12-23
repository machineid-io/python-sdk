# MachineID Python SDK

Official Python client for the MachineID device enforcement API.

MachineID lets you control whether a process, agent, or runtime is allowed to execute — in real time — using a simple register / validate model.  
It is commonly used to enforce AI agent limits, protect automation workloads, and centrally revoke execution authority.

## Install

pip install machineid-io

## Getting an Org Key

To use the SDK, you need an organization API key.

1. Sign up at https://machineid.io
2. Create an organization in the dashboard
3. Copy your org API key (starts with `org_...`)

You will use this key to authenticate all SDK calls.

## Initialize

from machineid_io.client import MachineIDClient

client = MachineIDClient(
    org_key="YOUR_ORG_KEY"
)

## Register Device (idempotent)

Registers a device or agent instance.  
Safe to call every time your process starts.

reg = client.register("agent-01")

if reg.get("status") not in ("ok", "exists"):
    raise RuntimeError(f"Register failed: {reg}")

print("Register success:", reg.get("status"))

## Validate (Runtime Gate)

This is the enforcement checkpoint.

Your process must stop immediately when `allowed` is False.

res = client.validate("agent-01")

if not res.allowed:
    print("Denied:", res.code, res.request_id)
    raise SystemExit(1)

### Validate Result Fields

- allowed — True or False
- code — Stable decision code (ALLOW, DEVICE_REVOKED, PLAN_FROZEN, etc.)
- request_id — Correlation ID for logs and support
- status, reason — Legacy fields (still included)
- raw — Full raw API response

## Revoke Device

Revokes execution authority.  
The device will be blocked on its next validate call.

client.revoke("agent-01")

## Unrevoke Device

Explicitly restores execution authority.

client.unrevoke("agent-01")

## List Devices

devices = client.list_devices()
print(devices)

## Enforcement Model

MachineID is an authority layer, not a process manager.

- Revoke = execution must stop
- Unrevoke does not auto-restart processes
- Validate is the single source of truth

Always gate execution on `validate()`.

## Links

- Dashboard: https://machineid.io/dashboard
- Documentation: https://machineid.io/docs
- Pricing: https://machineid.io/pricing

## License

MIT
