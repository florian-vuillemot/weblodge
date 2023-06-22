from u_deploy._azure import AppService

from .resource_group import develop as rg_develop, staging as rg_staging, production as rg_production


develop = AppService(name='app-service', number_of_sites=2, sku='P1v3', resource_group=rg_develop, location='North Europe', id='/subscriptions/15be6804-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/develop/providers/Microsoft.Web/serverfarms/app-service')
staging = AppService(name='app-service', number_of_sites=1, sku='P1v3', resource_group=rg_staging, location='North Europe', id='/subscriptions/8615f926-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/staging/providers/Microsoft.Web/serverfarms/app-service')
production = AppService(name='app-service', number_of_sites=1, sku='P1v3', resource_group=rg_production, location='North Europe', id='/subscriptions/2f0df319-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/production/providers/Microsoft.Web/serverfarms/app-service')
