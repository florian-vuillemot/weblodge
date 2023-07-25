Delete
######

The *delete* operation deletes the infrastructure deployed but keeps the build.

Usage
*****

.. code-block:: console

   $ # Delete the application previously deployed.
   $ weblodge delete

   $ # Delete the application previously deployed without prompt.
   $ weblodge delete --yes


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
   * - yes
     - Do not prompt a validation message before deletion.
     - `false`
