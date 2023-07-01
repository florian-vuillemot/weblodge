from typing import Dict, List

from weblodge.config import Config, ConfigField

from .build import Build
from .deploy import Deploy


class WebApp:
    def __init__(self, config: Config) -> None:
        self._config = config

    def build(self) -> None:
        """
        Build the application.
        """
        build_config = self._user_config(Build.config())
        build = Build(**build_config)
        build.build()

    def deploy(self) -> str:
        """
        Deploy the application to Azure.
        Return the URL of the deployed application.
        """
        deploy_config = self._user_config(Deploy.config())
        deploy = Deploy(**deploy_config)
        return deploy.deploy()

    def config(self) -> Dict[str, List[ConfigField]]:
        """
        Configure the application.
        """
        return {
            'build': Build.config(),
            'deploy': Deploy.config()
        }
    
    def _user_config(self, fields: List[ConfigField]) -> Dict[str, str]:
        """
        Extract the user configuration from the config object.
        """
        return {f.name: self._config[f.name] for f in fields}
