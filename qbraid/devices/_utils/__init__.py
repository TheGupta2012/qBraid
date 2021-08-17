# pylint: skip-file

from tabulate import tabulate

from .aws_utils import (
    BRAKET_PROVIDERS,
    AWS_DEVICE_INFO,
    AWS_CONFIG_PROMPT,
    aws_config_path,
)

from .ibm_utils import (
    QISKIT_PROVIDERS,
    IBM_DEVICE_INFO,
    IBMQ_CONFIG_PROMPT,
)

from .google_utils import (
    CIRQ_PROVIDERS,
    GOOGLE_DEVICE_INFO,
)

from .user_config import set_config, get_config

SUPPORTED_VENDORS = {
    "aws": BRAKET_PROVIDERS,
    "google": CIRQ_PROVIDERS,
    "ibm": QISKIT_PROVIDERS,
}

DEVICE_INFO = {
    "aws": AWS_DEVICE_INFO,
    "google": GOOGLE_DEVICE_INFO,
    "ibm": IBM_DEVICE_INFO,
}

RUN_PACKAGE = {
    "aws": "braket",
    "google": "cirq",
    "ibm": "qiskit",
}

CONFIG_PROMPTS = {
    "aws": AWS_CONFIG_PROMPT,
    "google": None,
    "ibm": IBMQ_CONFIG_PROMPT,
}


def update_config(vendor):
    """Update the config associated with given vendor

    Args:
        vendor (str): a supported vendor

    """
    prompt_lst = CONFIG_PROMPTS[vendor]
    for prompt in prompt_lst:
        set_config(*prompt, update=True)
    return 0


def get_devices(provider=None, vendor=None, simulator=None, creds=None):
    """Prints all available devices, tabulated by provider and vendor. The user may filter results
    according to a particular device provider, software vendor, or simulators/non-simulators.

    Args:
        provider (optional, str): the name of a device provider
        vendor (optional, str): the name of a software vendor
        simulator (optional, bool): filter for simulators
        creds (optional, bool): filter for devices that require credentials to use

    """
    device_list = []
    for vendor_key in SUPPORTED_VENDORS:
        if vendor is None or vendor == vendor_key:
            for provider_key in SUPPORTED_VENDORS[vendor_key]:
                if provider is None or provider == provider_key:
                    for device_key in SUPPORTED_VENDORS[vendor_key][provider_key]:
                        if simulator is None or simulator == (device_key.find("sim") != -1):
                            device_ref = SUPPORTED_VENDORS[vendor_key][provider_key][device_key]
                            if creds is None or creds == isinstance(device_ref, str):
                                device_info = DEVICE_INFO[vendor_key][device_key]
                                device_info.append(device_key)
                                device_list.append(device_info)
    if len(device_list) == 0:
        print("No devices found matching given criteria.")
    else:
        print(tabulate(
            device_list,
            headers=["Provider", "Device Name", "Num Qubits", "qBraid ID"]
        ))