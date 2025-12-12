import os
from machineid_io import MachineID

def main() -> None:
    org_key = os.getenv("MACHINEID_ORG_KEY")
    if not org_key:
        raise RuntimeError("Set MACHINEID_ORG_KEY in your environment")

    client = MachineID(org_key)

    print("=== /usage ===")
    usage = client.usage()
    print(usage)

    device_id = "sdk-test-device-01"

    print("\n=== /devices/register ===")
    reg = client.register(device_id)
    print(reg)

    print("\n=== /devices/validate ===")
    val = client.validate(device_id)
    print(val)

    print("\n=== /devices/list ===")
    devices = client.list_devices()
    print(devices)

if __name__ == "__main__":
    main()
