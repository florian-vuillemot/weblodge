from weblodge._azure import ResourceGroupModel


develop = ResourceGroupModel(name='develop', location='northeurope', tags={})
staging = ResourceGroupModel(name='staging', location='northeurope', tags={})
production = ResourceGroupModel(name='production', location='northeurope', tags={})
