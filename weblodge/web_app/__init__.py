"""
Wrapper around Azure Web App components and settings.
"""
from .web_app import deploy, deploy_config, delete_config, delete

from .logs import logs, config as logs_config

from .build import build, BuildConfig, BuildException, RequirementsFileNotFound
