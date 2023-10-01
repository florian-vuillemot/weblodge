.. _deploy:

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

.. note::

  **WebLodge** creates an `Azure Key Vault`_ and provides permissions to the deployer (ex: the GitHub Action) to set secrets and to the Azure WebApp running the application to read them.
  `Azure Key Vault`_ is not a free service, but in this context the cost is almost zero. Indeed, the cost is based on the number of operations. In this case, the number of operations is equal to the number of secrets by the number of restarts of the application and deployment.
  You can find more information on the `Azure Key Vault pricing page`_.


.. _python-dotenv: https://pypi.org/project/python-dotenv
.. _Azure Key Vault: https://learn.microsoft.com/en-us/azure/key-vault/general/basic-concepts
.. _Azure Key Vault pricing page: https://azure.microsoft.com/en-us/pricing/details/key-vault/


Building during deployment
**************************

You can build and then deploy your application by providing the `--build` option.
If you need to specify more options, you can add all the :ref:`build` options.

.. code-block:: console

   $ # Build then deploy the local application.
   $ weblodge deploy --build

   $ # Build the application with a custom folder then deploy.
   $ weblodge deploy --build --src myapp
