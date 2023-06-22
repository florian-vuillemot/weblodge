from u_deploy._azure import WebApp

from .app_services_plan import  develop as asp_develop, staging as asp_staging, production as asp_production, \
                                rg_develop, rg_staging, rg_production


develop = WebApp(
    name="develop-app-service",
    host_names=["develop-app-service.azurewebsites.net"],
    kind="app,linux,container",
    location="North Europe",
    linux_fx_version="DOCKER|develop-registry.azurecr.io/app-service:main",
    app_service=asp_develop,
    resource_group=rg_develop,
)
staging = WebApp(
    name="staging-app-service",
    host_names=["staging-app-service.azurewebsites.net"],
    kind="app,linux,container",
    location="North Europe",
    linux_fx_version="DOCKER|staging-registry.azurecr.io/app-service:main",
    app_service=asp_staging,
    resource_group=rg_staging
)
production = WebApp(
    name="production-app-service",
    host_names=["production-app-service.azurewebsites.net"],
    kind="app,linux,container",
    location="North Europe",
    linux_fx_version="DOCKER|production-registry.azurecr.io/app-service:main",
    app_service=asp_production,
    resource_group=rg_production
)