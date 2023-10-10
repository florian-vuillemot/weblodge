"""
These tests ensure the CLI's behavior in real-life conditions.
The tests consist of deploying and re-deploying an application on
the cloud and checking that it is accessible via HTTP.
"""
import os
import sys
import time
from pathlib import Path

from urllib3 import Retry, request

from weblodge.cli import main


# Tests update the application folder.
# Keep current allows to return to the starting point.
current_folder = os.getcwd()


def test(cmd, html_expected, log) -> str:
    """
    Deploy an application.
    """
    print(f'---------------------- {log} ----------------------')
    print(f'Running: {cmd}', flush=True)

    app_status = -1
    app_output = None

    # Simulate the CLI call.
    sys.argv = cmd.split()
    web_app = main(return_web_app=True)

    for _ in range(3):
        # Ensure the application is reachable.
        time.sleep(60)
        try:
            res = request(
                "GET",
                web_app.url(),
                retries=Retry(total=10, backoff_factor=5, status=5, status_forcelist=[500, 502, 503, 504])
            )
            app_output = res.data.decode('utf-8')
            app_status = res.status
        except Exception as e: # pylint: disable=invalid-name,broad-exception-caught
            print(f"Test failed.\nTraceback: {e}", flush=True, file=sys.stderr)

        if app_status < 400 and app_output == html_expected:
            # Setting env variable can take time.
            break
        else:
            print('Retrying...', flush=True)

    # Test the result.
    assert app_status < 400, f'The application is not reachable {app_status}.'
    assert app_output == html_expected, f'Unexpected output: {app_output}'

    print('-----------------------------------------------------')
    print('---------------------- Success ----------------------')
    print('-----------------------------------------------------\n\n\n', flush=True)
    return web_app.url()


try:
    # Create an env var file.
    Path('.env').write_text('RESULT=TEST env var.', encoding='utf-8')
    # B1 SKU is used for parallel testing.
    # Azure limits the `F1` SKU to one per region and per subscription.
    # Create the infrastructure and deploy the standard application with env variable.
    test(
        'weblodge deploy --src app_1 --build --tier B1',
        'TEST env var.',
        'Test env variable.'
    )
    # Deploy the same application with a different env variable.
    Path('.foo').write_text('RESULT="From foo."', encoding='utf-8')
    test(
        'weblodge deploy --src app_1 --build --tier B1 --env-file .foo',
        'From foo.',
        'Test specify env var variable.'
    )
    # Deploy another application on the same infrastructure.
    test(
        f'weblodge deploy --build --entry-point main.py --src app_2 --requirements r.txt --flask-app myapp',
        'From foo.',
        'Deploy another application.'
    )
except (SystemExit, Exception) as e: # pylint: disable=invalid-name,broad-exception-caught
    print(f"Test failed.\nTraceback: {e}", flush=True, file=sys.stderr)
finally:
    # Delete resources.
    sys.argv = ['weblodge', 'delete', '--yes']
    main()
