from .build import WebApp as WebAppBuilder
from .deploy import WebApp as WebAppDeploy

build = WebAppBuilder()
build.build()
WebAppDeploy().deploy(build.package_path)
