from _azure import Cli
from _azure import ResourceGroupHelper

cli = Cli()
v = ResourceGroupHelper(cli)

for i in v.list():
    print(i)
