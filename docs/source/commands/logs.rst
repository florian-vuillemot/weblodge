Logs
####

The *logs* operation streams your application logs. Because it is a stream, logs are truncated.

Usage
*****

.. code-block:: console

   $ # Print logs of the application previously created.
   $ weblodge logs


Details
*******

Logs can be buffered and never appear in the stream.

If you use the `print`_ method, you can force logs to be written to the console by sending them to the `stderr`_ output or by using the `flush` option.

If you use the `logging`_ module, only logs starting at the `WARNING` level will be displayed by default. Otherwise, update the `logging level`_ module to the required level.


.. _print: https://docs.python.org/3/library/functions.html#print
.. _stderr: https://docs.python.org/3/library/sys.html#sys.stderr
.. _logging: https://docs.python.org/3/library/logging.html
.. _logging level: https://docs.python.org/3/library/logging.html#logging.Logger.setLevel

Options
*******

.. list-table::
   :widths: 20 60 20
   :header-rows: 1

   * - Option name
     - Description
     - Default value
   * - subdomain
     - The subdomain of the application to be deleted.
     - `<my-subdomain>`
