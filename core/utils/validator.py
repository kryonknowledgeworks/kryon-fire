"""This file contains utility functions for validating data types."""
import re
from core.utils.vars import get_resource_schema, change_datatype_valid_format
from decimal import Decimal

error_details = dict()


def case_regex(value, regex):
    """Validate regex"""
    if isinstance(value, str) and re.fullmatch(regex, value):
        return True


def constant_validator(value, constant):
    """Validate constant"""
    if value == constant:
        return True


class TermValidator:
    def __init__(self):
        self.term = None
        self.datatype = None
        self.schema = None
        self.key = None
        self.value = None

    def initialize_term(self, datatype, term, value, key):
        """Initialize term"""
        default = "incorrect_term"
        self.value = value
        self.key = key
        self.datatype = datatype
        self.term = term
        return getattr(self, f'case_{datatype}', lambda: default)()

    def case_object(self):
        if not isinstance(self.value, change_datatype_valid_format(self.datatype)):
            DataTypeValidator().external_error_details({self.key: f"Only {self.datatype} is allowed. ({self.key})"})

        else:
            self.schema = get_resource_schema(f"term/{self.term}")
            for key in self.schema.keys():
                if self.schema[key].get('cardinality') == '1..1' and not self.value.get(key):
                    DataTypeValidator().external_error_details({key: f"Missing required field. ({key})"})

            for key, inside_value in self.value.items():
                if self.schema.get(key):
                    datatype = self.schema[key]['type']
                    DataTypeValidator().initialize_datatype(datatype=datatype, value=inside_value,
                                                            key=key,
                                                            regex=self.schema[key].get('regex'),
                                                            predefined_constants=self.schema[key].get(
                                                                'predefined_constants'),
                                                            multi_datatype=self.schema[key].get(
                                                                'multi_datatype'),
                                                            constant=self.schema[key].get('constant'),
                                                            ref=self.schema[key].get('ref'))

    def case_array(self):
        if not isinstance(self.value, change_datatype_valid_format(self.datatype)):
            DataTypeValidator().external_error_details({self.key: f"Only {self.datatype} is allowed. ({self.key})"})

        else:
            self.schema = get_resource_schema(f"term/{self.term}")
            for item in range(len(self.value)):

                for key in self.schema.keys():
                    if self.schema[key].get('cardinality') == '1..1' and not self.value[item].get(key):
                        DataTypeValidator().external_error_details(
                            {key: f"Missing required field. ({key})"})

                for key, inside_value in self.value[item].items():
                    if self.schema.get(key):
                        datatype = self.schema[key]['type']
                        DataTypeValidator().initialize_datatype(datatype=datatype, value=inside_value,
                                                                key=key,
                                                                regex=self.schema[key].get('regex'),
                                                                predefined_constants=self.schema[key].get(
                                                                    'predefined_constants'),
                                                                multi_datatype=self.schema[key].get(
                                                                    'multi_datatype'),
                                                                constant=self.schema[key].get('constant'),
                                                                ref=self.schema[key].get('ref'))


class DataTypeValidator:
    """Validate all data types"""

    def __init__(self):
        self.predefined_constants = None
        self.multi_datatype = None
        self.key = None
        self.constant = None
        self.regex = None
        self.value = None

    def initialize_datatype(self, datatype, value, key,
                            regex=None, predefined_constants=None,
                            multi_datatype=None,
                            constant=None, ref=None):
        """Initialize datatype"""
        default = "incorrect_datatype"
        if ref:
            TermValidator().initialize_term(datatype=datatype, term=ref, value=value, key=key)
        self.value = value
        self.regex = regex
        self.key = key
        self.predefined_constants = predefined_constants
        self.multi_datatype = multi_datatype
        self.constant = constant
        return getattr(self, 'case_' + str(datatype), lambda: default)()

    def case_string(self):
        """Validate string data type"""
        str_check = isinstance(self.value, str)

        if str_check:
            if self.regex and not case_regex(self.value, self.regex):
                error_details[self.key] = "Regex not matched."

            if self.constant and not constant_validator(self.value, self.constant):
                error_details[self.key] = f"Constant not matched ({self.constant})."
        else:
            error_details[self.key] = "Only allowed string data type."

        return error_details.get(self.key)

    def case_integer(self):
        """Validate integer data type"""
        int_check = isinstance(self.value, int)
        if int_check:
            if self.constant and not constant_validator(self.value, self.constant):
                error_details[self.key] = f"Constant not matched ({self.constant})."
        else:
            error_details[self.key] = "Only allowed integer data type."

        return error_details.get(self.key)

    def case_positive_int(self):
        if isinstance(self.value, int) and self.value > 0:
            ...
        else:
            error_details[self.key] = "Only allowed positive integer data type."

        return error_details.get(self.key)

    def case_integer64(self):
        """Validate integer data type"""
        self.case_integer()

    def case_decimal(self):
        """Validate decimal data type"""
        if not Decimal(self.value):
            error_details[self.key] = "Only allowed decimal data type."

    def case_markdown(self):
        """Validate markdown data type"""
        return self.case_string()

    def case_uri(self):
        """Validate uri data type"""
        return self.case_string()

    def case_code(self):
        """Validate uri data type"""
        return self.case_string()

    def case_string_array(self):
        """Validate array string data type"""
        if not isinstance(self.value, list):
            error_details[self.key] = "Only allowed array data type."
        else:
            res = False in [isinstance(i, str) for i in self.value]
            if res:
                error_details[self.key] = "Only allowed array contains string data type."

        return error_details.get(self.key)

    def case_date(self):
        """Validate date data type"""
        if isinstance(self.value, str) and re.fullmatch(self.regex, self.value):
            ...
        else:
            error_details[self.key] = "Invalid date format."

        return error_details.get(self.key)

    def case_date_time(self):
        """Validate date time data type"""
        if isinstance(self.value, str) and re.fullmatch(self.regex, self.value):
            ...
        else:
            error_details[self.key] = "Invalid date time format."

        return error_details.get(self.key)

    def case_boolean(self):
        """Validate boolean data type"""
        if not isinstance(self.value, bool):
            error_details[self.key] = "Only allowed boolean data type."

        return error_details.get(self.key)

    def case_predefined_constants(self):
        """Validate predefined constants"""
        if isinstance(self.value, str) and self.value in self.predefined_constants:
            ...
        else:
            error_details[
                self.key] = (f"Chosen value is not in predefined"
                             f" constants {tuple(self.predefined_constants)}.")

        return error_details.get(self.key)

    def case_multi_datatype(self):
        """Validate multiple data type"""
        checklist = []
        datatype_store = []

        for multi_type in self.multi_datatype:
            datatype_store.append(multi_type.get("type"))
            if True not in checklist:
                if self.initialize_datatype(datatype=multi_type.get("type"), value=self.value, key=self.key,
                                            regex=multi_type.get("regex")) is None:
                    checklist.append(True)
                else:
                    error_details.pop(self.key)

        if True not in checklist:
            error_details[self.key] = "Only allowed data type is " + str(tuple(datatype_store))

    def external_error_details(self, external_error):
        """Update error details"""
        error_details.update(external_error)

    def validation_report(self):
        """Return error details"""
        return error_details

    def reset_error_details(self):
        """Reset error details"""
        global error_details
        error_details = {}
