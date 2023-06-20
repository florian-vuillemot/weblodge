from _azure import Cli
from _azure import ResourceGroupHelper, AppServiceHelper, WebAppHelper

cli = Cli()
rg = ResourceGroupHelper(cli)
ap = AppServiceHelper(cli)
wa = WebAppHelper(cli)

rg.create('develop-tmp', 'North Europe')
ap.create('app-develop-tmp', 'B1', rg)
wa.create('webapp-develop-tmp', ap)
