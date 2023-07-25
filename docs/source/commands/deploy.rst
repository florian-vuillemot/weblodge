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

.. _computational power: https://azure.microsoft.com/en-us/pricing/details/app-service/linux/

.. note::
   
   WebLodge considers the `subdomain` as the application name.
