from _azure import Cli
from _azure import AppService, AppServiceHelper

cli = Cli()
v = AppServiceHelper(cli)

for i in v.list():
    print(i)
