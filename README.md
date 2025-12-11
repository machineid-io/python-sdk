# MachineID.io Python SDK

Official Python client for the MachineID.io API.

This SDK provides a thin wrapper around the core device and usage endpoints:

- POST /api/v1/devices/register  
- GET  /api/v1/devices/validate  
- GET  /api/v1/devices/list  
- POST /api/v1/devices/revoke  
- POST /api/v1/devices/unrevoke  
- POST /api/v1/devices/remove  
- GET  /api/v1/usage  

All calls use the `x-org-key` header and return the raw JSON from the API.

---

## Installation

For now, install by cloning the repo and installing dependencies manually:

    git clone https://github.com/machineid-io/python-sdk.git
    cd python-sdk
    pip install requests

(Once published to PyPI, this will switch to `pip install machineid`.)

---

## Quick Start

    from machineid import MachineID

    client = MachineID("org_1234567890abcdef")
    device_id = "agent-01"

    # Check usage / plan limits
    usage = client.usage()
    print("Plan:", usage["planTier"], "Limit:", usage["limit"])

    # Register a device (idempotent)
    reg = client.register(device_id)
    print("Register status:", reg["status"])

    # Validate before performing work
    val = client.validate(device_id)
    if val.get("allowed"):
        print("Device allowed:", val.get("reason"))
    else:
        print("Device blocked:", val.get("reason"))

---

## API Methods

All methods require an `org_key`:

    from machineid import MachineID
    client = MachineID("org_1234567890abcdef")

### `usage()`

    usage = client.usage()
    print(usage)

Returns plan tier, plan state, access clock, device counts, and limit status.

---

### `register(device_id: str)`

    reg = client.register("agent-01")
    print(reg)

Returns one of:

- `ok`  
- `exists`  
- `restored`  
- `limit_reached`

---

### `validate(device_id: str)`

    val = client.validate("agent-01")
    print(val)

Use this before agents perform major tasks.

---

### `list_devices()`

    devices = client.list_devices()
    print(devices)

Returns all active + revoked devices.

---

### Device management

    client.revoke("agent-01")
    client.unrevoke("agent-01")
    client.remove("agent-01")

- `revoke` → soft ban  
- `unrevoke` → restore  
- `remove` → hard delete  

---

## Environment-Based Setup

    # export MACHINEID_ORG_KEY=org_123...
    from machineid import MachineID

    client = MachineID.from_env()

---

## License

MIT – see `LICENSE`.
