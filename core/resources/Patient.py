from core.DomainResource import DomainResource
from core.utils.validator import DataTypeValidator
from core.utils.vars import get_resource_schema


class Patient(DomainResource):

    def __init__(self, resource):
        self.validation_report = None
        print("From ===> class Patient")
        super().__init__(resource)
        self.resource = resource
        self.schema = get_resource_schema("patient")
        self.do_validate()

    def do_validate(self):

        for key in self.schema.keys():
            if self.schema[key].get('cardinality') == '1..1' and not self.resource.get(key):
                DataTypeValidator().external_error_details({key: f"Missing required field. ({key})"})

            if self.resource.get(key):
                datatype = self.schema[key]['type']

                DataTypeValidator().initialize_datatype(datatype=datatype, value=self.resource[key], key=key,
                                                        regex=self.schema.get(key=key).get('regex'),
                                                        predefinedConstants=self.schema.get(key=key).get(
                                                            'predefinedConstants'),
                                                        multi_datatype=self.schema.get(key=key).get('multi_datatype'),
                                                        constant=self.schema.get(key=key).get('constant'))

    def validation_result(self):
        self.validation_report = DataTypeValidator().validation_report()
        DataTypeValidator().reset_error_details()
        return self.validation_report