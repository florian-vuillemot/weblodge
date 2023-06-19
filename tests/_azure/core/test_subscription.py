import json
import unittest
from pathlib import Path

from u_deploy._azure.core.subscription import Subscription, SubscriptionHelper

from .cli import Cli


subscriptions_json = json.loads(Path('./tests/_azure/core/subscriptions.json').read_text())

class TestSubscription(unittest.TestCase):
    def setUp(self) -> None:
        self.cli = Cli()
        self.subscription_helper = SubscriptionHelper(self.cli)
        self.cli.add_command('account list', subscriptions_json)
        return super().setUp()

    def test_list_subscription(self):
        expected_output = [
            Subscription(id='15be6804-xxxx-xxxx-xxxx-xxxxxxxxxxxx', name='develop'),
            Subscription(id='8615f926-xxxx-xxxx-xxxx-xxxxxxxxxxxx', name='staging'),
            Subscription(id='2f0df319-xxxx-xxxx-xxxx-xxxxxxxxxxxx', name='production'),
        ]

        r = self.subscription_helper.list()

        self.assertEqual(expected_output, r)

    def test_get_subscription(self):
        name = 'staging'
        expected_output = Subscription(id='8615f926-xxxx-xxxx-xxxx-xxxxxxxxxxxx', name=name)

        r = self.subscription_helper.get(name)

        self.assertEqual(expected_output, r)
