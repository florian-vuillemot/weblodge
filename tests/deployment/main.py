"""
These tests ensure the CLI's behavior in real-life conditions.
Each test consists of deploying an application on the cloud and
checking that it is accessible via HTTP.
"""
import os
import random
import string
import sys
import time
import shutil
import importlib

from urllib3 import Retry, request

from weblodge.cli import main
from weblodge.web_app.deploy import DeploymentConfig


# Tests update the application folder.
# Keep current allows to return to the starting point.
current_folder = os.getcwd()


def test(folder, cmd, log):
    """
    Deploy application by going in the `folder` and running the `cmd`.
    Automatic delete the infrastructure at the end.
    """
    print(f'---------------------- {log} ----------------------')
    print(f'Running: {cmd}', flush=True)

    app_reached = False
    os.chdir(folder)

    # Simulate the CLI call.
    sys.argv = cmd.split()
    web_app = main()

    # Ensure the application is reachable.
    time.sleep(30)
    try:
        app_reached = request("GET", web_app.url(), retries=Retry(total=10, backoff_factor=5)).status < 400
    except Exception as e: # pylint: disable=invalid-name,broad-exception-caught
        print(f"Test failed.\nTraceback: {e}", flush=True, file=sys.stderr)

    # Delete resources.
    sys.argv = ['weblodge', 'delete', '--yes']
    main()

    # Delete test files.
    shutil.rmtree('dist')
    os.unlink('.weblodge.json')

    # Go back to the original folder.
    os.chdir(current_folder)

    # Test failed, exit with an error.
    assert app_reached

    print('-----------------------------------------------------')
    print('---------------------- Success ----------------------')
    print('-----------------------------------------------------\n\n\n', flush=True)


# B1 SKU is used for parallel testing.
# Azure limits the `F1` SKU to one per region and per subscription.
test('app', 'weblodge deploy --build --sku B1', 'No parameters provided.')
app = ''.join(random.choice(string.ascii_lowercase) for _ in range(20))  # pylint: disable=invalid-name
test('.', f'weblodge deploy --build --src app --sku B1 --app {app}', 'Specifies the source folder and the app name.')
