"""
These tests ensure the CLI's behavior in real-life conditions.
Test consists of running the `app-tiers` command and check the output.
"""
import io
import sys
from contextlib import redirect_stdout, redirect_stderr

from weblodge.cli import main


def run_app_tiers(args: str) -> (str, str, bool):
    """
    Run the `app-tiers` command with options and print outputs.
    """
    sys_exit = False

    print('--------------------------------------------')
    print(f"Running: weblodge app-tiers '{args}'", flush=True)

    # Simulate the CLI call.
    sys.argv = ['weblodge', 'app-tiers', *args.split()]
    with redirect_stdout(io.StringIO()) as fstdout:
        with redirect_stderr(io.StringIO()) as fstderr:
            try:
                main()
            except SystemExit:
                sys_exit = True

    print('--------------- stdout ------------------')
    stdout = fstdout.getvalue()
    print(stdout)
    print('--------------- stderr ------------------')
    stderr = fstderr.getvalue()
    print(stderr)
    return stdout, stderr, sys_exit

# Default location.
bstdout, bstderr, bsys_exit = run_app_tiers('')
assert 'B1' in bstdout
assert 'Warning: There is no guarantee of the estimated price.' in bstdout
assert bstderr == ''
assert not bsys_exit

# Custom location.
wstdout, wstderr, wsys_exit = run_app_tiers('--location westus')
assert 'B1' in wstdout
assert 'Warning: There is no guarantee of the estimated price.' in wstdout
assert wstderr == ''
assert not wsys_exit
assert wstdout != bstdout

# Exit on error.
istdout, istderr, isys_exit = run_app_tiers('--location incorrect')
assert 'B1' not in istdout
assert 'Warning: There is no guarantee of the estimated price.' not in istdout
assert 'Can not find any tier for the provided location.' in istderr
assert isys_exit
