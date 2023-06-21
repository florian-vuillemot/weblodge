import unittest

from u_deploy._azure.core.subscription import Subscription, SubscriptionHelper

from .cli import cli


class TestSubscription(unittest.TestCase):
    def setUp(self) -> None:
        self.subscription_helper = SubscriptionHelper(cli)
        return super().setUp()

    def test_list(self):
        expected_output = [
            Subscription(id='15be6804-xxxx-xxxx-xxxx-xxxxxxxxxxxx', name='develop'),
            Subscription(id='8615f926-xxxx-xxxx-xxxx-xxxxxxxxxxxx', name='staging'),
            Subscription(id='2f0df319-xxxx-xxxx-xxxx-xxxxxxxxxxxx', name='production'),
        ]

        r = self.subscription_helper.list()

        self.assertEqual(expected_output, r)

    def test_get(self):
        name = 'staging'
        expected_output = Subscription(id='8615f926-xxxx-xxxx-xxxx-xxxxxxxxxxxx', name=name)

        r = self.subscription_helper.get(name)

        self.assertEqual(expected_output, r)
