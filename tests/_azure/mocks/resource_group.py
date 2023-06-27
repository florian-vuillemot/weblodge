from u_deploy._azure import ResourceGroupModel


develop = ResourceGroupModel(name='develop', location='northeurope')
staging = ResourceGroupModel(name='staging', location='northeurope')
production = ResourceGroupModel(name='production', location='northeurope')
