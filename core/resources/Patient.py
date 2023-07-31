import this

from core.DomainResource import DomainResource
from core.utils.resource_validator import is_common_resource_validation
from core.utils.vars import get_patient_schema


class Patient(DomainResource):
    resource = None
    schema = get_patient_schema()


def do_validate():
    pass


def __init__(self, resource):
    print("From ===> class Patient")
    super().__init__(resource)
    self.resource = resource
    do_validate()
