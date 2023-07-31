from core.BaseResource import BaseResource


class DomainResource(BaseResource):
    def __init__(self, resource):
        super().__init__(resource)
        print("From ===> class Domain Resource")
        print(resource)
