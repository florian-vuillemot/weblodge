# pylint: disable=line-too-long
"""
Default App Service Plan Mocks.
"""
from weblodge._azure import AppServiceModel

from .resource_group import develop as rg_develop, staging as rg_staging, production as rg_production


develop = AppServiceModel(
    name='app-service',
    number_of_sites=2,
    sku='P1v3',
    resource_group=rg_develop,
    location='North Europe',
    id='/subscriptions/15be6804-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/develop/providers/Microsoft.Web/serverfarms/app-service',
    tags={}
)
staging = AppServiceModel(
    name='app-service',
    number_of_sites=1,
    sku='P1v3',
    resource_group=rg_staging,
    location='North Europe',
    id='/subscriptions/8615f926-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/staging/providers/Microsoft.Web/serverfarms/app-service',
    tags={}
)
production = AppServiceModel(
    name='app-service',
    number_of_sites=1,
    sku='P1v3',
    resource_group=rg_production,
    location='North Europe',
    id='/subscriptions/2f0df319-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/production/providers/Microsoft.Web/serverfarms/app-service',
    tags={}
)
