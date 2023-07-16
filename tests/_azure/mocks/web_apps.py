"""
Default Web App Mocks.
"""
from weblodge._azure import WebAppModel

from .app_services_plan import  develop as asp_develop, staging as asp_staging, production as asp_production, \
                                rg_develop, rg_staging, rg_production


develop = WebAppModel(
    name="develop-app-service",
    domain="develop-app-service.azurewebsites.net",
    kind="app,linux,container",
    location="North Europe",
    linux_fx_version="DOCKER|develop-registry.azurecr.io/app-service:main",
    app_service=asp_develop,
    resource_group=rg_develop,
    tags={
      "environment": "develop",
      "usage": "monitor"
    },
)
staging = WebAppModel(
    name="staging-app-service",
    domain="staging-app-service.azurewebsites.net",
    kind="app,linux,container",
    location="North Europe",
    linux_fx_version="DOCKER|staging-registry.azurecr.io/app-service:main",
    app_service=asp_staging,
    resource_group=rg_staging,
    tags={
      "environment": "staging",
      "usage": "monitor"
    },
)
production = WebAppModel(
    name="production-app-service",
    domain="production-app-service.azurewebsites.net",
    kind="app,linux,container",
    location="North Europe",
    linux_fx_version="DOCKER|production-registry.azurecr.io/app-service:main",
    app_service=asp_production,
    resource_group=rg_production,
    tags={
      "environment": "production",
      "usage": "monitor"
    },
)
