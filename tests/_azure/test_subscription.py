"""
Subscription Tests.
"""
import unittest

from weblodge._azure import SubscriptionModel, Subscription

from .cli import cli


class TestSubscription(unittest.TestCase):
    """
    Subscription CRUD Tests.
    """
    def setUp(self) -> None:
        self.subscription = Subscription(cli)
        return super().setUp()

    def test_list(self):
        """
        Ensure the corresponding conversion is done by the `list` method.
        """
        expected_output = [
            SubscriptionModel(id='15be6804-xxxx-xxxx-xxxx-xxxxxxxxxxxx', name='develop'),
            SubscriptionModel(id='8615f926-xxxx-xxxx-xxxx-xxxxxxxxxxxx', name='staging'),
            SubscriptionModel(id='2f0df319-xxxx-xxxx-xxxx-xxxxxxxxxxxx', name='production'),
        ]

        self.assertEqual(expected_output, self.subscription.list())

    def test_get(self):
        """
        Ensure the `get` method returns the corresponding Subscription.
        """
        name = 'staging'
        expected_output = SubscriptionModel(id='8615f926-xxxx-xxxx-xxxx-xxxxxxxxxxxx', name=name)

        self.assertEqual(expected_output, self.subscription.get(name))
