The configuration file
######################

At the end of a deployment, **WebLodge** creates a file named `.weblodge.json` by default.
This file contains the previous configuration, enabling **WebLodge** to update your application with the same parameters.
This file can be version-controlled and used in your Continuous Deployment.

Usage
*****

.. code-block:: console

   $ weblodge build --config-file myconfigfile.json

Options
*******

.. list-table::
   :widths: 20 60 20
   :header-rows: 1

   * - Option name
     - Description
     - Default value
   * - config-file
     - The configuration file path.
     - `.weblodge.json`
