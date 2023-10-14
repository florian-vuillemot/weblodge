"""
Abstract representation of an Azure resource.
"""
import time
import logging
from typing import Dict, Optional
from abc import abstractmethod
from collections import UserDict

from .cli import Cli
from .exceptions import AzureException, CanLoadResource

logger = logging.getLogger('weblodge')


class _AzDict(UserDict):
    """
    Lazy loader of the Azure resource.
    """
    def __init__(self, load: callable, **kwargs):
        super().__init__(**kwargs)
        self._load = load

    def __getitem__(self, key):
        if not self.data:
            self._load()
        return super().__getitem__(key)


class Resource:
    """
    Abstract representation of an Azure resource.
    """
    # Prefix used with the Azure CLI.
    # Ex:
    # - 'webapp' for Azure WebApp.
    # - 'appservice plan' for Azure AppService Plan.
    _cli: Optional[Cli] = None
    _cli_prefix: Optional[str] = None
    _internal_tags = {'managedby': 'weblodge'}

    def __init__(self, name: str, from_az: Optional[Dict] = None) -> None:
        self.name = name
        self._from_az = _AzDict(load=self.load, **(from_az or {}))

    @property
    def _user_id(self) -> str:
        """
        Return ID of the current user.
        """
        return self._invoke('account show')['user']['name']

    @property
    def tags(self) -> Dict[str, str]:
        """
        Return the resource tags.
        """
        return self._from_az['tags']

    def __eq__(self, other: 'Resource') -> bool:
        return other.name == self.name

    def load(self):
        """
        Load the resource from Azure.
        It automatically retries if the command fails.
        """
        return self._retry(
            self._load,
            f"Cannot load resource '{self.name}' from Azure.",
            CanLoadResource
        )

    def exists(self) -> bool:
        """
        Return True if the resource exists.
        Load the resource from Azure if found.
        """
        for resource in self.all():
            if resource == self:
                self._from_az.update(resource._from_az) # pylint: disable=protected-access
                return True
        return False

    @classmethod
    def all(cls):
        """
        Return all resources managed by WebLodge.
        """
        resources = cls._invoke(
            f'{cls._cli_prefix} list'
        )

        # Tags must be present and not None.
        ressources_with_tags = (_r for _r in resources if _r.get('tags'))
        weblodges_resources = (_r for _r in ressources_with_tags if _r['tags'].get('managedby') == 'weblodge')
        yield from (
            cls.from_az(_r['name'], _r) for _r in weblodges_resources
        )

    @classmethod
    def set_cli(cls, cli: Cli):
        """
        Set the Azure CLI.
        """
        cls._cli = cli

    @classmethod
    def _invoke(cls, *args, **kwargs):
        """
        Return the Azure CLI invoke method.
        Can be transform in operator when support of python3.8 is dropped.
        """
        if cls._cli is None:
            cls._cli = Cli()
        return cls._cli.invoke(*args, **kwargs)

    @classmethod
    @abstractmethod
    def from_az(cls, name: str, from_az: Dict):
        """
        Create the resource from Azure.
        """

    @abstractmethod
    def _load(self):
        """
        Load the resource from Azure.
        """

    # pylint: disable=keyword-arg-before-vararg,too-many-arguments
    @classmethod
    def _retry(
            cls,
            fct,
            log_msg: str,
            exception: AzureException,
            retry: int = 10,
            *args,
            **kwargs
        ):
        """
        Try to execute the given function and retry if it fails.
        """
        try:
            return fct(*args, **kwargs)
        except Exception as raised:  # pylint: disable=broad-exception-caught
            if retry > 0:
                time.sleep(5)
                return cls._retry(
                    fct=fct,
                    log_msg=log_msg,
                    exception=exception,
                    retry=retry - 1,
                    *args,
                    **kwargs
                )
            logger.error(log_msg)
            logger.exception(raised)
            raise exception(log_msg) from raised
