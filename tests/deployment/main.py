"""
These tests ensure the CLI's behavior in real-life conditions.
Each test consists of deploying an application on the cloud and
checking that it is accessible via HTTP.
"""
import os
import sys
import json
import sleep
import shutil

from weblodge.cli import main
from weblodge._azure import Cli, WebApp
from weblodge.web_app.deploy import Deploy


# Tests update the application folder.
# Keep current allows to return to the starting point.
current_folder = os.getcwd()


def test(folder, cmd, log):
    """
    Deploy application by going in the `folder` and running the `cmd`.
    Automatic delete the infrastructure at the end.
    """
    print(f'---------------------- {log} ----------------------')
    print(f'Running: {cmd}')

    app_reached = False
    os.chdir(folder)

    # Simulate the CLI call.
    sys.argv = cmd.split()
    main()

    # Ensure the application is reachable.
    sleep.time(30)
    try:
        with open('.weblodge.json', 'r', encoding='utf-8') as genereated_config:
            web_app = WebApp(Cli()).get(
                json.load(genereated_config)['app_name']
            )
        app_reached = Deploy().ping(web_app)
    except Exception as e: # pylint: disable=invalid-name,broad-exception-caught
        print(f"Test failed.\nFolder: '{folder}'\nCMD: '{cmd}'\nTraceback: {e}")

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
    print('-----------------------------------------------------\n\n\n')


# B1 SKU is used for parallel testing.
# Azure limits the `F1` SKU to one per region and per subscription.
test('app', 'weblodge deploy --build --sku B1', 'No parameters provided.')
test('.', 'weblodge deploy --build --src app --sku B1', 'Specifies the source folder.')
