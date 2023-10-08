"""
These tests ensure the CLI's behavior in real-life conditions.
Each test consists of deploying an application on the cloud and
checking that it is accessible via HTTP.
"""
import io
import sys
from contextlib import redirect_stdout, redirect_stderr

from weblodge.cli import main


def run_app_tiers(args: str) -> (str, str, bool):
    """
    Deploy application by going in the `folder` and running the `cmd`.
    Automatic delete the infrastructure at the end.
    """
    sys_exit = False

    print('--------------------------------------------')
    print(f"Running: weblodge --app-tiers '{args}'", flush=True)

    # Simulate the CLI call.
    sys.argv = ['weblodge', 'app-tiers', *args.split()]
    with redirect_stdout(io.StringIO()) as fstdout:
        with redirect_stderr(io.StringIO()) as fstderr:
            try:
                main()
            except SystemExit:
                sys_exit = True

    return fstdout.getvalue(), fstderr.getvalue(), sys_exit

stdout, stderr, sys_exit = run_app_tiers('')
print(stdout), print(stderr), print(sys_exit)
assert 'B1' in stdout
assert 'Warning: There is no guarantee of the estimated price.' in stdout
assert stderr == ''
assert not sys_exit