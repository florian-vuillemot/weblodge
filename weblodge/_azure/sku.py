"""
SKU class for Azure resources.
"""
from decimal import Decimal
from dataclasses import dataclass
from typing import Iterable

from urllib3 import Retry, request

from .interfaces import AzureAppServiceSku


_B_TIER = "Designed for apps that have lower traffic requirements, and don't need advanced auto scale and traffic management features."  # pylint: disable=line-too-long
_S_TIER = "Designed for running production workloads"
_PV3_TIER = "Designed to provide enhanced performance for production apps and workloads."

_SKU_INFOS = {
    'F1': {'cores': '60 CPU minutes / day', 'ram': '1', 'disk': '1', 'description': 'Free Tier for testing.'},

    'B1': {'cores': '1', 'ram': '1.75', 'disk': '10', 'description': _B_TIER},
    'B2': {'cores': '2', 'ram': '3.50', 'disk': '10', 'description': _B_TIER},
    'B3': {'cores': '4', 'ram': '7', 'disk': '10', 'description': _B_TIER},

    'S1': {'cores': '1', 'ram': '1.75', 'disk': '50', 'description': _S_TIER},
    'S2': {'cores': '2', 'ram': '3.50', 'disk': '50', 'description': _S_TIER},
    'S3': {'cores': '4', 'ram': '7', 'disk': '50', 'description': _S_TIER},

    'P0v3': {'cores': '1', 'ram': '4', 'disk': '250', 'description': _PV3_TIER},
    'P1v3': {'cores': '2', 'ram': '8', 'disk': '250', 'description': _PV3_TIER},
    'P1mv3': {'cores': '2', 'ram': '16', 'disk': '250', 'description': _PV3_TIER},
    'P2v3': {'cores': '4', 'ram': '16', 'disk': '250', 'description': _PV3_TIER},
    'P2mv3': {'cores': '4', 'ram': '32', 'disk': '250', 'description': _PV3_TIER},
    'P3v3': {'cores': '8', 'ram': '32', 'disk': '250', 'description': _PV3_TIER},
    'P3mv3': {'cores': '8', 'ram': '64', 'disk': '250', 'description': _PV3_TIER},
    'P4mv3': {'cores': '16', 'ram': '128', 'disk': '250', 'description': _PV3_TIER},
    'P5mv3': {'cores': '32', 'ram': '256', 'disk': '250', 'description': _PV3_TIER},
}

AVAILABLE_SKUS = list(_SKU_INFOS.keys())


@dataclass(frozen=True)
class AppServiceSku(AzureAppServiceSku):
    """
    Human representation of the SKU.
    """
    # Name of the SKU.
    name: str
    # Name of the region where the SKU is available.
    region: str
    # Price per hour of the SKU.
    price_by_hour: Decimal
    # Human description of the SKU.
    description: str
    # Number of Cores.
    cores: int
    # RAM in GB.
    ram: str
    # Disk size in GB.
    disk: str


def get_skus(region_name: str) -> Iterable[AzureAppServiceSku]:
    """
    Return the list of available SKUs for the given region.
    """
    try:
        skus = request(
            'GET',
            f"https://prices.azure.com/api/retail/prices?$filter=serviceName eq 'Azure App Service' and contains(productName, 'Linux') and armRegionName eq '{region_name}' and unitOfMeasure eq '1 Hour' and type eq 'Consumption' and isPrimaryMeterRegion eq true and currencyCode eq 'USD'",  # pylint: disable=line-too-long
            retries=Retry(total=10, backoff_factor=5, status=5, status_forcelist=[500, 502, 503, 504])
        )
        items = skus.json()['Items']
    except:  # pylint: disable=bare-except
        print(f"""Unable to retrieve the list of SKUs.
Please check your internet connection and the location '{region_name}'.""")

    for item in items:
        sku_info = _SKU_INFOS.get(item['skuName'])

        if sku_info:
            yield AppServiceSku(
                name=item['skuName'],
                region=item['armRegionName'],
                price_by_hour=Decimal(item['retailPrice']),
                description=sku_info['description'],
                cores=int(sku_info['cores']),
                ram=sku_info['ram'],
                disk=sku_info['disk']
            )
