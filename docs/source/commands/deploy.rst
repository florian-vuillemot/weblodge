Deploy
######

The *deploy* operation creates the necessary infrastructure and uploads the build package - i.e. your code - on the infrastructure.

Usage
*****

.. code-block:: console

   $ # Deploy the local application.
   $ weblodge deploy

   $ # Deploy the local application with a custom subdomain.
   $ weblodge deploy --subdomain myapp


Options
*******

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
   * - env-file
     - Path to the environment file.
     - `.env`

.. _computational power: https://azure.microsoft.com/en-us/pricing/details/app-service/linux/

.. note::
   
   WebLodge considers the `subdomain` as the application name.


Environment variables
*********************

If your application needs environment variables, you can provide them in
a `.env` file or by providing the `--env-file` option.

.. code-block:: console

   $ # Deploy the local application using the '.env' file.
   $ cat .env
    MY_VAR=foo
   $ weblodge deploy

   $ # Deploy the local application with a custom file containing environment variables.
   $ cat prod.env
    MY_VAR=foo
   $ weblodge deploy --env-file prod.env

.. note::

  **WebLodge** is using the `python-dotenv`_ package to load environment variables and so support all it functionality.

.. _python-dotenv: https://pypi.org/project/python-dotenv


Building during deployment
**************************

You can build and then deploy your application by providing the `--build` option.
If you need to specify more options, you can add all the *build* options.

.. code-block:: console

   $ # Build then deploy the local application.
   $ weblodge deploy --build

   $ # Build the application with a custom folder then deploy.
   $ weblodge deploy --build --src myapp
