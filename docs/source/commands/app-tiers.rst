App-tiers
#########

The *app-tiers* operation returns all application tiers available from **WebLodge** in the selected region.
The output is a list of application tiers, each with a description and hardware information.

Usage
*****

.. code-block:: console

   $ weblodge app-tiers
   Warning: There is no guarantee of the estimated price.

   Tier description: Designed to provide enhanced performance for production apps and workload.
   Tier location: northeurope
    Name |    Price    | Cores |   RAM   | Storage
   -----------------------------------------------
    P0v3 |  $0.11/hour |     1 |    4 GB |  250 GB
   P1mv3 |  $0.20/hour |     2 |   16 GB |  250 GB
   P2mv3 |  $0.40/hour |     4 |   32 GB |  250 GB
   P3mv3 |  $0.81/hour |     8 |   64 GB |  250 GB
   P4mv3 |  $1.61/hour |    16 |  128 GB |  250 GB
   P5mv3 |  $3.23/hour |    32 |  256 GB |  250 GB

   Tier description: Designed for running production workloads
   Tier location: northeurope
    Name |    Price    | Cores |   RAM   | Storage
   -----------------------------------------------
   S1 |  $0.10/hour |     1 | 1.75 GB |   50 GB
   S2 |  $0.19/hour |     2 |  3.5 GB |   50 GB
   S3 |  $0.38/hour |     4 |    7 GB |   50 GB

   Tier description: Designed for apps with lower traffic requirements and not needing advanced auto scale and traffic management features.
   Tier location: northeurope
    Name |    Price    | Cores |   RAM   | Storage
   -----------------------------------------------
   B1 |  $0.02/hour |     1 | 1.75 GB |   10 GB
   B2 |  $0.04/hour |     2 |  3.5 GB |   10 GB
   B3 |  $0.07/hour |     4 |    7 GB |   10 GB


.. note::

  Prices are in USD and estimated from Azure APIs. There is no guarantee that the prices are correct.


Option
*******

.. list-table::
   :widths: 20 60 20
   :header-rows: 1

   * - Option name
     - Description
     - Default value
   * - location
     - Fetch information from the designed region.
     - `northeurope`

.. note::

   **WebLodge** will use the location in :ref:`the configuration file <config-file>` if defined and not overridden via the command line.
