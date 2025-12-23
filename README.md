# MachineID Python SDK

Official Python client for the MachineID device enforcement API.

## Install

pip install machineid-io

## Initialize

from machineid_io.client import MachineIDClient

client = MachineIDClient(
    org_key="YOUR_ORG_KEY"
)

## Register Device

Idempotent. Safe to call every time your agent starts.

client.register("agent-01")

## Validate (Runtime Gate)

This is the enforcement checkpoint.  
Your process must stop immediately when allowed is False.

res = client.validate("agent-01")

if not res.allowed:
    print("Denied:", res.code, res.request_id)
    raise SystemExit(1)

### Validate Result Fields

<<<<<<< HEAD
# Register device (idempotent)
reg = client.register(device_id)

if reg["status"] not in ("ok", "exists"):
    raise RuntimeError(f"Register failed: {reg}")

print("Register success:", reg["status"])
=======
- allowed — True or False  
- code — Stable decision code (ALLOW, DEVICE_REVOKED, PLAN_FROZEN, etc.)  
- request_id — Correlation ID for logs and support  
- status, reason — Legacy fields (still included)  
- raw — Full raw API response  
>>>>>>> 78df738 (Python SDK: POST validate + decision codes + request_id)

## Revoke Device

Stops the device on its next validate call.

client.revoke("agent-01")

## Unrevoke Device

Explicitly re-grants execution authority.

client.unrevoke("agent-01")

## List Devices

devices = client.list_devices()
print(devices)

## Enforcement Model

MachineID is an authority layer, not a process manager.

- Revoke = execution must stop  
- Unrevoke does not auto-restart  
- Validate is the single source of truth  

Always gate execution on validate().

## License

MIT
