"""
Internal Azure interface.

This package is for internal use only and must not be use from a third package.
"""
from .cli import Cli
from .subscription import SubscriptionModel, Subscription
from .appservice import AppServiceModel, AppService
from .resource_group import ResourceGroupModel, ResourceGroup
from .web_app import WebAppModel, WebApp
