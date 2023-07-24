Commands
########

Build
*****

The *build* operation collects and prepares the application for deployment on a specific platform.

Usage
=====

.. code-block:: console

   $ # Build the local application.
   $ weblodge build

   $ # Build the application in the 'myapp' folder.
   $ weblodge build --src myapp


Details
=======

This command is sensible to the application structure. Applications must follow the pre-defined pattern or specify custom values.

Here is an example of the standard pattern deployable without configuration:

.. code-block:: console

   $ cat app.py  # The application entry point.
   from flask import Flask

   app = Flask(__name__)  # The Flask application.

   @app.route("/")
   def hello_world():
      return "<p>Hello, World!</p>"

It can be deployed with:

.. code-block:: console

   $ weblodge deploy --build

Here is a non-standard example:

.. code-block:: console

   $ cat main.py  # The application entry point.
   from flask import Flask

   my_app = Flask(__name__)  # The Flask application.

   @app.route("/")
   def hello_world():
      return "<p>Hello, World!</p>"

To be able to deploy the application, you must first *build* it and specify:
- The entry point file: `main.py`.
- The **Flask** application: `my_app`.

.. code-block:: console

   $ # Build the application.
   $ weblodge build --entry-point main.py --flask-app my_app
   $ # Deploy the application.
   $ weblodge deploy


Options
=======

.. list-table::
   :widths: 20 60 20
   :header-rows: 1

   * - Option name
     - Description
     - Default value
   * - src
     - Folder containing application sources.
     - `.` (current folder)
   * - dist
     - Folder containing the application built.
     - `dist`
   * - entry-point
     - The application file to be executed with `python`.
     - `app.py`
   * - flask-app
     - The Flask application object in the `entry-point` file.
     - `app`
   * - requirements
     - The *requirements.txt* file path of the application. Ignores if a `requirements.txt` file is located at the root of the application.
     - `requirements.txt`


Deploy
******

The *deploy* operation creates the necessary infrastructure and uploads the build package - i.e. your code - on the infrastructure.

Usage
=====

.. code-block:: console

   $ # Deploy the local application.
   $ weblodge deploy

   $ # Deploy the local application with a custom subdomain.
   $ weblodge deploy --subdomain myapp


Options
=======

.. list-table::
   :widths: 20 60 20
   :header-rows: 1

   * - Option name
     - Description
     - Default value
   * - subdomain
     - The subdomain of the application on the Internet: `<subdomain>.azurewebsites.net`. Randomly generated if not provided.
     - `<randomly generated>`
   * - sku
     - The application `computational power`_.
     - `F1`
   * - location
     - The physical application location.
     - `northeurope`
   * - environment
     - The environment of your application.
     - `production`
   * - build
     - Build the application before deployment.
     - `false`
   * - dist
     - Folder containing the application built.
     - `dist`

.. _computational power: https://azure.microsoft.com/en-us/pricing/details/app-service/linux/

.. note::
   
   WebLodge considers the `subdomain` as the application name.


Delete
******

The *delete* operation deletes the infrastructure deployed but keeps the build.

Usage
=====

.. code-block:: console

   $ # Delete the application previously deployed.
   $ weblodge delete

   $ # Delete the application previously deployed without prompt.
   $ weblodge delete --yes


Options
=======

.. list-table::
   :widths: 20 60 20
   :header-rows: 1

   * - Option name
     - Description
     - Default value
   * - subdomain
     - The subdomain of the application to be deleted.
     - `<my-subdomain>`
   * - yes
     - Do not prompt a validation message before deletion.
     - `false`


Logs
****

The *logs* operation streams your application logs. Because it is a stream, logs are truncated.

Usage
=====

.. code-block:: console

   $ # Print logs of the application previously created.
   $ weblodge logs


Details
=======

Logs can be buffered and never appear in the stream.

If you use the `print`_ method, you can force logs to be written to the console by sending them to the `stderr`_ output or by using the `flush` option.

If you use the `logging`_ module, only logs starting at the `WARNING` level will be displayed by default. Otherwise, update the `logging level`_ module to the required level.


.. _print: https://docs.python.org/3/library/functions.html#print
.. _stderr: https://docs.python.org/3/library/sys.html#sys.stderr
.. _logging: https://docs.python.org/3/library/logging.html
.. _logging level: https://docs.python.org/3/library/logging.html#logging.Logger.setLevel

Options
=======

.. list-table::
   :widths: 20 60 20
   :header-rows: 1

   * - Option name
     - Description
     - Default value
   * - subdomain
     - The subdomain of the application to be deleted.
     - `<my-subdomain>`


Configuration file
******************

At the end of a deployment, **WebLodge** creates a file named `.weblodge.json` by default.
This file contains the previous configuration, enabling **WebLodge** to update your application with the same parameters.
This file can be version-controlled and used in your Continuous Deployment.

Usage
=====

.. code-block:: console

   $ weblodge build --config-file myconfigfile.json

Options
=======

.. list-table::
   :widths: 20 60 20
   :header-rows: 1

   * - Option name
     - Description
     - Default value
   * - config-file
     - The configuration file path.
     - `.weblodge.json`

