from typing import Dict, List

from weblodge.config import Field as ConfigField

from .build import Build
from .deploy import Deploy


class WebApp:
    def build(self, config: Dict[str, str]) -> None:
        """
        Build the application.
        """
        build = Build(**config)
        build.build()

    def deploy(self, config: Dict[str, str]) -> str:
        """
        Deploy the application to Azure.
        Return the URL of the deployed application.
        """
        deploy = Deploy(**config)
        return deploy.deploy()

    def config(self) -> Dict[str, List[ConfigField]]:
        """
        Configure the application.
        """
        return {
            'build': Build.config(),
            'deploy': Deploy.config(),
        }
