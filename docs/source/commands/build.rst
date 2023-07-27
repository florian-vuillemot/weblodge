.. _build:

Build
#####

The *build* operation collects and prepares the application for deployment on a specific platform.

Usage
*****

.. code-block:: console

   $ # Build the local application.
   $ weblodge build

   $ # Build the application in the 'myapp' folder.
   $ weblodge build --src myapp


Details
*******

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
*******

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
