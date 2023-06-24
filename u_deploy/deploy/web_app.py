from dataclasses import dataclass

from u_deploy._azure import Cli, ResourceGroupHelper, AppServiceHelper, WebAppHelper


@dataclass
class WebApp:
    def deploy(self, src: str) -> None:
        """
        Deploy the application to Azure.
        """
        cli = Cli()
        rg = ResourceGroupHelper(cli)
        wa = WebAppHelper(cli)
        ap = AppServiceHelper(cli)

        _rg = rg.create('develop-tmp', 'northeurope')
        _ap = ap.create('app-develop-tmp', 'B1', _rg)
        _wa = wa.create('webapp-develop-tmp', _ap)

        wa.deploy(_wa, src)
