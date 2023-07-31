from core.DomainResource import DomainResource
from core.utils.validator import DataTypeValidator
from core.utils.vars import get_patient_schema


class Patient(DomainResource):

    def __init__(self, resource):
        print("From ===> class Patient")
        super().__init__(resource)
        self.resource = resource
        self.schema = get_patient_schema()
        self.do_validate()

    def do_validate(self):

        for key in self.schema.keys():

            if self.resource.get(key):
                datatype = self.schema[key]['type']

                DataTypeValidator().initialize_datatype(datatype=datatype,
                                                        value=self.resource[key], key=key,
                                                        regex=self.schema.get(key=key).get('regex'),
                                                        predefinedConstants=self.schema.get(key=key).get(
                                                            'predefinedConstants'),
                                                        multi_datatype=self.schema.get(key=key).get('multi_datatype'))
