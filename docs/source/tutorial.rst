Tutorial
========

This tutorial will demonstrate using **WebLodge** to deploy a simple application.

Standard application
********************

Here is the application we will deploy:

.. code-block:: console

   $ # The application entry point.
   $ cat app.py 
   from flask import Flask

   app = Flask(__name__)  # The Flask application.

   @app.route("/")
   def hello_world():
      return "<p>Hello, World!</p>"

   $ # The application dependencies.
   $ cat requirements.txt 
   Flask

You can deploy this application by executing the following commands in a terminal:

.. code-block:: console

   $ # Install WebLodge.
   $ pip install weblodge

   $ # Build the application.
   $ weblodge build
   $ weblodge deploy
   ...
   The application will soon be available at: https://weblodge-tutorial.azurewebsites.net

   $ # But you can also build and deploy the application in a single command.
   $ weblodge deploy --build
   ...
   The application will soon be available at: https://weblodge-tutorial.azurewebsites.net

During the build phase, **WebLodge** will create a folder with the application built and other files needed to deploy the application. This private folder does not need to be versioned and ignored by your version control system.

**WebLodge** will create a `.weblodge.json` file containing the application's deployment configuration during deployment. This file can be version control.
The application needs a subdomain on the internet -- here `weblodge-tutorial` --.
This subdomain is unique on Azure. You can set it by passing the `--subdomain` option. Otherwise, **WebLodge** will generate one.

After a few seconds, the application will be available at the given subdomain and accessible from your browser.

.. note::

    The `.weblodge.json` contains the subdomain of the application. This subdomain
    is unique on Azure. However, another application might already use, making it unavailable. If this is the case, you can change the subdomain in the
    `.weblodge.json` file and redeploy the application.

.. warning::

    By default, **WebLodge** will deploy free resources. This means Azure will shut down the application after a couple of minutes of inactivity, and the usage will be limited daily. You can change this behaviour by passing the `--sku` option.
    Azure limits the number of free applications. If you encounter that problem, please remove the previously created resources or deploy and change the `--sku` option.

Adding environment variables
****************************

Your application may use environment variables containing dynamic values or secrets.
For example, we can update the `app.py` file to return a message that depends on the `MESSAGE` environment variable:

.. code-block:: console

    $ cat app.py
    import os
    from flask import Flask

    app = Flask(__name__)  # The Flask application.

    @app.route("/")
    def hello_world():
      return f"<p>Hello, {os.environ['MESSAGE']}!</p>"


By default, **WebLodge** will see if the `.env` file exists, and if so, use it for environment variables.
You can also specify this file by using the `--env-file` option:

.. code-block:: console

    $ cat .env
    MESSAGE=World
    $ # Deploy the application using the `.env` file.
    $ weblodge deploy
    ...
    The application will soon be available at: https://weblodge-tutorial.azurewebsites.net
    $ curl https://weblodge-tutorial.azurewebsites.net
    Hello, World

    $ cat .prod
    MESSAGE=Guido
    $ # Deploy the application using the `.prod` file.
    $ weblodge deploy --env-file .prod
    ...
    The application will soon be available at: https://weblodge-tutorial.azurewebsites.net
    $ curl https://weblodge-tutorial.azurewebsites.net
    Hello, Guido

.. note::

    Environment variables are defined during the deployment phase. You don't need to rebuild the application to change them.

Behind the scene, **WebLodge** uses the `python-dotenv`_ package to load the environment variables. Feel free to use its features.

.. _python-dotenv: https://pypi.org/project/python-dotenv


Deleting the infrastructure
***************************

You can delete the previously deployed infrastructure by executing the following commands in a terminal:

.. code-block:: console

    $ # With the validation prompt.
    $ weblodge delete
    Do you want to delete the application 'weblodge-tutorial' (yes/no.)?

    $ # Without the validation prompt.
    $ weblodge delete --yes
