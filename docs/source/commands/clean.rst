Clean
######

The *clean* operation deletes all infrastructure deployed by **WebLodge**.
The user is asked to confirm before deleting.

Usage
*****

.. code-block:: console

   $ weblodge clean
   Are you sure you want to delete the application 'my-weblodge-app' (yes/no.)? no
   Aborting.
   Are you sure you want to delete the application 'my-other-weblodge-app' (yes/no.)? yes
   Deleting...
   Successfully deleted


.. note::

  Because of the risk of data loss, the *clean* operation always displays a confirmation prompt.
