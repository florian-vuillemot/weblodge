from typing import Dict, List

from u_deploy.config import Config, ConfigField

from .build import Build
from .deploy import Deploy


class WebApp:
    def __init__(self, config: Config) -> None:
        self._config = config

    def build(self) -> None:
        """
        Build the application.
        """
        build = Build(src=self._config['src'], dest=self._config['dest'])
        build.build()

    def deploy(self) -> str:
        """
        Deploy the application to Azure.
        Return the URL of the deployed application.
        """
        deploy = Deploy(
            app_name=self._config['app-name'],
            sku=self._config['sku'],
            location=self._config['location']

        )
        return deploy.deploy()

    def config(self) -> Dict[str, List[ConfigField]]:
        """
        Configure the application.
        """
        return {
            'build': Build.config(),
            'deploy': Deploy.config(),
            'delete': Delete.config()
        }