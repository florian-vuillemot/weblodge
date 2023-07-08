"""
Wrapper around Azure Web App components and settings.
"""
from .web_app import build, build_config, \
    deploy, deploy_config, delete_config, delete

from .logs import logs, config as logs_config
