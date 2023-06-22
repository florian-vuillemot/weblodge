from u_deploy._azure import ResourceGroup


develop = ResourceGroup(name='develop', location='northeurope')
staging = ResourceGroup(name='staging', location='northeurope')
production = ResourceGroup(name='production', location='northeurope')
