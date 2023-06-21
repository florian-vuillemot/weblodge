from ._azure import Cli
from ._azure import ResourceGroupHelper, AppServiceHelper, WebAppHelper

cli = Cli()
rg = ResourceGroupHelper(cli)
ap = AppServiceHelper(cli)
wa = WebAppHelper(cli)

# _rg = rg.create('develop-tmp', 'northeurope')
# _ap = ap.create('app-develop-tmp', 'B1', _rg)
# _wa = wa.create('webapp-develop-tmp', _ap)

_rg = rg.get('develop-tmp', 'northeurope')
_ap = ap.get('app-develop-tmp', _rg)
_wa = wa.get('webapp-develop-tmp')


wa.delete(_wa)
ap.delete(_ap)
rg.delete(_rg)