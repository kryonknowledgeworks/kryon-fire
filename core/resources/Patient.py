from core.DomainResource import DomainResource
from core.utils.vars import get_patient_schema


class Patient(DomainResource):
    resource = None

    def __init__(self, resource):
        print("From ===> class Patient")
        super().__init__(resource)
        self.resource = resource
        self.schema = get_patient_schema()
        self.do_validate()

    def do_validate(self):
        for key in self.schema.keys():
            print(self.schema.get(key=key).get('type'))
