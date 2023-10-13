"""
SKU class for Azure resources.
"""
from dataclasses import dataclass
from typing import Iterable

from urllib3 import Retry as urllib_retry, request as urllib_request

from .interfaces import AzureAppServiceSku
from .exceptions import InvalidSku, InvalidLocation


# Function to use for HTTP calls and mocks.
RETRY = urllib_retry
REQUEST = urllib_request

# Tier description of SKU families.
_F_TIER = 'Free tier - limited to 60 minutes per day.'
_B_TIER = 'Designed for apps with lower traffic requirements and not needing advanced auto scale and traffic management features.'  # pylint: disable=line-too-long
_S_TIER = 'Designed for running production workloads.'
_PV3_TIER = 'Designed to provide enhanced performance for production apps and workload.'

# Hard coded hardware capabilities for each SKU.
_SKU_INFOS = {
    'F1': {'cores': 1, 'ram': 1, 'disk': 1, 'description': _F_TIER},

    'B1': {'cores': 1, 'ram': 1.75, 'disk': 10, 'description': _B_TIER},
    'B2': {'cores': 2, 'ram': 3.50, 'disk': 10, 'description': _B_TIER},
    'B3': {'cores': 4, 'ram': 7, 'disk': 10, 'description': _B_TIER},

    'S1': {'cores': 1, 'ram': 1.75, 'disk': 50, 'description': _S_TIER},
    'S2': {'cores': 2, 'ram': 3.50, 'disk': 50, 'description': _S_TIER},
    'S3': {'cores': 4, 'ram': 7, 'disk': 50, 'description': _S_TIER},

    'P0v3': {'cores': 1, 'ram': 4, 'disk': 250, 'description': _PV3_TIER},
    'P1v3': {'cores': 2, 'ram': 8, 'disk': 250, 'description': _PV3_TIER},
    'P1mv3': {'cores': 2, 'ram': 16, 'disk': 250, 'description': _PV3_TIER},
    'P2v3': {'cores': 4, 'ram': 16, 'disk': 250, 'description': _PV3_TIER},
    'P2mv3': {'cores': 4, 'ram': 32, 'disk': 250, 'description': _PV3_TIER},
    'P3v3': {'cores': 8, 'ram': 32, 'disk': 250, 'description': _PV3_TIER},
    'P3mv3': {'cores': 8, 'ram': 64, 'disk': 250, 'description': _PV3_TIER},
    'P4mv3': {'cores': 16, 'ram': 128, 'disk': 250, 'description': _PV3_TIER},
    'P5mv3': {'cores': 32, 'ram': 256, 'disk': 250, 'description': _PV3_TIER},
}

# List of available SKU names.
AVAILABLE_SKUS = list(_SKU_INFOS.keys())


@dataclass(frozen=True)
class AppServiceSku(AzureAppServiceSku):
    """
    User representation of the SKU.
    """
    # Name of the SKU.
    name: str

    # Name of the location where the SKU is available.
    location: str

    # Price per hour of the SKU.
    price_by_hour: float

    # Description of the SKU.
    description: str

    # Number of Cores.
    cores: int

    # RAM in GB.
    ram: int

    # Disk size in GB.
    disk: int


def get_skus(location: str) -> Iterable[AzureAppServiceSku]:
    """
    Return availables SKUs for the given location.
    """
    try:
        # Retrieve SKUs from the Azure API.
        skus = REQUEST(
            'GET',
            f"https://prices.azure.com/api/retail/prices?$filter=serviceName eq 'Azure App Service' and contains(productName, 'Linux') and armRegionName eq '{location}' and unitOfMeasure eq '1 Hour' and type eq 'Consumption' and isPrimaryMeterRegion eq true and currencyCode eq 'USD'",  # pylint: disable=line-too-long
            retries=RETRY(total=10, backoff_factor=5, status=5, status_forcelist=[500, 502, 503, 504])
        )
        items = skus.json()['Items']
    except Exception as exception:  # pylint: disable=bare-except
        raise InvalidSku("""Unable to retrieve the list of SKUs.
Please check your internet connection."""
        ) from exception

    # The 'Items' key is empty when the location does not exist.
    if len(items) == 0:
        raise InvalidLocation(f"Can not find any SKU for the location '{location}'.")

    # Return each SKU as AppServiceSKU if find in the hard coded database.
    for item in items:
        sku_info = _SKU_INFOS.get(item['skuName'])

        if sku_info:
            yield AppServiceSku(
                name=item['skuName'],
                location=item['armRegionName'],
                price_by_hour=item['retailPrice'],
                description=sku_info['description'],
                cores=sku_info['cores'],
                ram=sku_info['ram'],
                disk=sku_info['disk']
            )

    # Return the free SKU.
    yield AppServiceSku(
        name='F1',
        location=location,
        price_by_hour=0.0,
        description=_SKU_INFOS['F1']['description'],
        cores=_SKU_INFOS['F1']['cores'],
        ram=_SKU_INFOS['F1']['ram'],
        disk=_SKU_INFOS['F1']['disk']
    )
