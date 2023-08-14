.. _github:

GitHub
######

The *github* command creates a GitHub workflow and the Azure infrastructure for continuous delivery from GitHub Actions.


Usage
*****

.. code-block:: console

   $ # Create the GitHub workflow that deploys the application of the user weblodge-org
   $ # on the repository weblodge on each push on main.
   $ weblodge github --username weblodge-org --repository weblodge --branch main
   Please, commit the following files:
     - .github/workflows/weblodge.yml
     - .weblodge.json
   And add the following secrets to your GitHub repository:
     - AZURE_CLIENT_ID: xxxxxxxxx-xxxx-xxxx-xxxxx-xxxxxxxxxxxx
     - AZURE_TENANT_ID: xxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
     - AZURE_SUBSCRIPTION_ID: xxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   More information: https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository


   $ # Same example but specifying the entry point file of the application.
   $ weblodge github --username weblodge-org --repository weblodge --branch main --entry-point myapp
   Please, add the following secrets to your GitHub repository:
      - AZURE_CLIENT_ID: xxxxxxxxx-xxxx-xxxx-xxxxx-xxxxxxxxxxxx
      - AZURE_TENANT_ID: xxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
      - AZURE_SUBSCRIPTION_ID: xxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    Then, commit and push the following files:
      - .github/workflows/weblodge.yml
      - .weblodge.json
   More information: https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository


Where:

- The file `.github/workflows/weblodge.yml` is the GitHub workflow.
- The file `.weblodge.json` contains the application configuration.
- `AZURE_CLIENT_ID`, `AZURE_TENANT_ID` and `AZURE_SUBSCRIPTION_ID` are the GitHub configuration for the Azure authentification and must be added as `GitHub secret`_.

.. note::

    Only a push on the specified branch will trigger the deployment.


.. _GitHub secret: https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository


Options
*******

.. list-table::
   :widths: 20 60 20
   :header-rows: 1

   * - Option name
     - Description
     - Default value
   * - username
     - The GitHub username/organisation.
     -
   * - repository
     - The repository that contains the application and the GitHub workflow.
     -
   * - branch
     - The branch that will trigger the workflow.
     -
   * - delete
     - Delete the generated Azure client. Do not delete the infrastructure.
     - False

You can also provide all options of the :ref:`build` and :ref:`deploy` commands.
Weblodge will use those options during the deployment from GitHub.

.. note::

    In this scenario, environment variables are not yet supported.


Details
*******

This command performs the following actions:

- Create the basic free infrastructure on Azure.
- Create the client that will deploy the application.
- Create the deployment GitHub workflow.

The client can deploy the application on the infrastructure on a limited scope.
Its authentification is via `federated credentials`_ with no password or certificate stored on GitHub.

.. _federated credentials: https://learn.microsoft.com/en-us/graph/api/resources/federatedidentitycredentials-overview?view=graph-rest-1.0
