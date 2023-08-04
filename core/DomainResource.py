from core.BaseResource import BaseResource


class DomainResource(BaseResource):
    """Domain Resource Class"""
    def __init__(self, resource):
        super().__init__(resource)
        print("From ===> class Domain Resource")
