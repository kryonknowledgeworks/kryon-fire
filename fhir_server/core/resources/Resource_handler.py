"""This class validates the Patient resource"""""
from fhir_server.core.DomainResource import DomainResource
from fhir_server.core.utils.validator import DataTypeValidator
from fhir_server.core.utils.vars import get_resource_schema


class ResourceHandler(DomainResource):
    """This class validates the Patient resource"""

    def __init__(self, resource, resource_type):
        self.validation_report = None
        print("From ===> class Patient")
        super().__init__(resource)
        self.resource = resource
        self.schema = get_resource_schema(resource_type)
        self.do_validate()

    def do_validate(self):
        """This method validates the resource"""
        try:
            if not self.schema:
                DataTypeValidator().external_error_details({"resourceType": "Resource not found"})
            else:
                for key in self.schema.keys():
                    if self.schema.get(key).get('cardinality') == '1..1' and not self.resource.get(key):
                        DataTypeValidator().external_error_details({key: f"Missing required field. ({key})"})

                for key, value in self.resource.items():

                    if self.schema.get(key):
                        datatype = self.schema.get(key)['type']

                        DataTypeValidator().initialize_datatype(datatype=datatype, value=value, key=key,
                                                                regex=self.schema[key].get('regex'),
                                                                predefined_constants=self.schema[key].get(
                                                                    'predefined_constants'),
                                                                multi_datatype=self.schema[key].get('multi_datatype'),
                                                                constant=self.schema[key].get('constant'),
                                                                ref=self.schema[key].get('ref'),
                                                                inside_type=self.schema[key].get('inside_type'),
                                                                ref_regex=self.schema[key].get('ref_regex'))
        except Exception as e:
            DataTypeValidator().external_error_details({"error": str(e)})

    def validation_result(self):
        """This method returns the validation report"""
        self.validation_report = DataTypeValidator().validation_report()
        DataTypeValidator().reset_error_details()
        return self.validation_report
