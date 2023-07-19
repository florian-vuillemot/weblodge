"""
Abstract representation of an Azure resource.
"""
import time
import logging
from typing import Dict
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
    def __init__(self, name: str, cli: Cli = Cli(), from_az: Dict = None) -> None:
        self.name = name
        self._cli = cli
        self._from_az = _AzDict(load=self.load, **(from_az or {}))

    @property
    def tags(self) -> Dict[str, str]:
        """
        Return the resource tags.
        """
        return self._from_az['tags']

    def __eq__(self, other: object) -> bool:
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
        """
        try:
            self._load()
            return True
        except Exception:  # pylint: disable=broad-exception-caught
            return False

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
