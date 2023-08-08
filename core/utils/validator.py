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
    """Validate term"""

    def __init__(self):
        self.ref_regex = None
        self.list_item = None
        self.validate_array_msg = None
        self.validate_msg = None
        self.key_tree = None
        self.term = None
        self.datatype = None
        self.schema = None
        self.key = None
        self.value = None

    def initialize_term(self, datatype, term, value, key, key_tree=None, list_item=None, ref_regex=None):
        """Initialize term"""
        default = "incorrect_term"
        self.value = value
        self.key = key
        self.ref_regex = ref_regex
        self.key_tree = key_tree
        self.datatype = datatype
        self.term = term
        self.list_item = list_item
        return getattr(self, f'case_{datatype}', lambda: default)()

    def case_object(self):
        """Validate object"""
        self.key_tree = self.key_tree if self.key_tree else self.key

        if not isinstance(self.value, change_datatype_valid_format(self.datatype)):
            self.key_tree = self.key_tree if self.key_tree else self.key

            DataTypeValidator().external_error_details(
                {self.key_tree: f"Only {self.datatype} is allowed. ({self.key})"})

        else:
            self.schema = get_resource_schema(f"term/{self.term}")

            for key in self.schema.keys():
                if self.schema[key].get('cardinality') == '1..1' and not self.value.get(key):

                    if self.list_item or self.list_item == 0:
                        adding_msg = f"/[{self.list_item}]/" + key
                    else:
                        adding_msg = "/" + key

                    self.key_tree = self.key_tree + adding_msg if self.key_tree else key
                    DataTypeValidator().external_error_details({self.key_tree: f"Missing required field. ({key})"})

            for key, inside_value in self.value.items():
                if self.schema.get(key):

                    if self.list_item or self.list_item == 0:
                        adding_msg = f"/[{self.list_item}]/" + key
                    else:
                        adding_msg = "/" + key

                    self.key_tree = self.key_tree + adding_msg if self.key_tree else self.key

                    datatype = self.schema[key]['type']
                    self.validate_msg = DataTypeValidator().initialize_datatype(datatype=datatype, value=inside_value,
                                                                                key=key,
                                                                                regex=self.schema[key].get('regex'),
                                                                                predefined_constants=self.schema[
                                                                                    key].get(
                                                                                    'predefined_constants'),
                                                                                multi_datatype=self.schema[key].get(
                                                                                    'multi_datatype'),
                                                                                constant=self.schema[key].get(
                                                                                    'constant'),
                                                                                ref=self.schema[key].get('ref'),
                                                                                key_tree=self.key_tree,
                                                                                inside_type=self.schema[key].get(
                                                                                    'inside_type'),
                                                                                ref_regex=self.ref_regex)
                    self.key_tree = self.key_tree.replace(adding_msg, "")

        return self.validate_msg

    def case_array(self):
        self.key_tree = self.key_tree if self.key_tree else self.key

        if not isinstance(self.value, change_datatype_valid_format(self.datatype)):
            DataTypeValidator().external_error_details(
                {self.key_tree: f"Only {self.datatype} is allowed. ({self.key})"})

        else:
            for item in range(len(self.value)):
                self.validate_array_msg = TermValidator().initialize_term(datatype="object", term=self.term,
                                                                          value=self.value[item], key=self.key,
                                                                          key_tree=self.key_tree, list_item=item,
                                                                          ref_regex=self.ref_regex)

        return self.validate_msg


class DataTypeValidator:
    """Validate all data types"""

    def __init__(self):
        self.ref_regex = None
        self.inside_type = None
        self.key_tree = None
        self.predefined_constants = None
        self.multi_datatype = None
        self.key = None
        self.constant = None
        self.regex = None
        self.value = None

    def initialize_datatype(self, datatype, value, key,
                            regex=None, predefined_constants=None,
                            multi_datatype=None,
                            constant=None, ref=None, key_tree=None, inside_type=None, ref_regex=None):
        """Initialize datatype"""
        default = "incorrect_datatype"

        if ref:
            TermValidator().initialize_term(datatype=datatype, term=ref, value=value, key=key, key_tree=key_tree,
                                            ref_regex=ref_regex)
        self.value = value
        self.regex = regex
        self.ref_regex = ref_regex
        self.key = key
        self.key_tree = key_tree
        self.inside_type = inside_type
        self.predefined_constants = predefined_constants
        self.multi_datatype = multi_datatype
        self.constant = constant
        return getattr(self, 'case_' + str(datatype), lambda: default)()

    def case_string(self):
        """Validate string data type"""
        str_check = isinstance(self.value, str)

        if str_check:
            if self.regex and not case_regex(self.value, self.regex):
                self.key_tree = self.key_tree if self.key_tree else self.key
                error_details[self.key_tree] = "Regex not matched."

            if self.constant and not constant_validator(self.value, self.constant):
                self.key_tree = self.key_tree if self.key_tree else self.key
                error_details[self.key_tree] = f"Constant not matched ({self.constant})."

            if self.ref_regex and self.key == "reference" and not case_regex(self.value, self.ref_regex):
                self.key_tree = self.key_tree if self.key_tree else self.key
                error_details[self.key_tree] = "Ref Regex not matched."
        else:
            self.key_tree = self.key_tree if self.key_tree else self.key
            error_details[self.key_tree] = "Only allowed string data type."

        return error_details.get(self.key_tree)

    def case_integer(self):
        """Validate integer data type"""
        int_check = isinstance(self.value, int)

        if int_check:
            if self.constant and not constant_validator(self.value, self.constant):
                self.key_tree = self.key_tree if self.key_tree else self.key
                error_details[self.key_tree] = f"Constant not matched ({self.constant})."

        else:
            self.key_tree = self.key_tree if self.key_tree else self.key
            error_details[self.key_tree] = "Only allowed integer data type."

        return error_details.get(self.key_tree)

    def case_positive_int(self):
        """Validate integer data type"""
        if isinstance(self.value, int) and self.value > 0:
            ...
        else:
            self.key_tree = self.key_tree if self.key_tree else self.key
            error_details[self.key_tree] = "Only allowed positive integer data type."

        return error_details.get(self.key_tree)

    def case_integer64(self):
        """Validate integer data type"""
        return self.case_integer()

    def case_decimal(self):
        """Validate decimal data type"""
        if not Decimal(self.value):
            self.key_tree = self.key_tree if self.key_tree else self.key
            error_details[self.key_tree] = "Only allowed decimal data type."

        return error_details.get(self.key_tree)

    def case_unsigned_int(self):
        """Validate integer data type"""
        if isinstance(self.value, int) and self.value >= 0:
            ...
        else:
            self.key_tree = self.key_tree if self.key_tree else self.key
            error_details[self.key_tree] = "Only allowed unsigned integer data type."

        return error_details.get(self.key_tree)

    def case_markdown(self):
        """Validate markdown data type"""
        return self.case_string()

    def case_uri(self):
        """Validate uri data type"""
        return self.case_string()

    def case_url(self):
        """Validate uri data type"""
        return self.case_string()

    def case_code(self):
        """Validate uri data type"""
        return self.case_string()

    def case_inside_array(self):
        """Validate array string data type"""
        if not isinstance(self.value, list):
            self.key_tree = self.key_tree if self.key_tree else self.key
            error_details[self.key_tree] = "Only allowed array data type."
        else:
            for i in self.value:
                if not isinstance(i, change_datatype_valid_format(self.inside_type)):
                    self.key_tree = self.key_tree if self.key_tree else self.key
                    error_details[self.key_tree] = "Only allowed array contains string data type."
                    break
                else:
                    if self.regex and not case_regex(i, self.regex):
                        self.key_tree = self.key_tree if self.key_tree else self.key
                        error_details[self.key_tree] = "Regex not matched."
                        break

        return error_details.get(self.key_tree)

    def case_date(self):
        """Validate date data type"""
        if isinstance(self.value, str) and re.fullmatch(self.regex, self.value):
            ...
        else:
            self.key_tree = self.key_tree if self.key_tree else self.key
            error_details[self.key_tree] = "Invalid date format."

        return error_details.get(self.key_tree)

    def case_date_time(self):
        """Validate date time data type"""
        if isinstance(self.value, str) and re.fullmatch(self.regex, self.value):
            ...
        else:
            self.key_tree = self.key_tree if self.key_tree else self.key
            error_details[self.key_tree] = "Invalid date time format."

        return error_details.get(self.key_tree)

    def case_time(self):
        """Validate time data type"""
        if isinstance(self.value, str) and re.fullmatch(self.regex, self.value):
            ...
        else:
            self.key_tree = self.key_tree if self.key_tree else self.key
            error_details[self.key_tree] = "Invalid time format."

        return error_details.get(self.key_tree)

    def case_boolean(self):
        """Validate boolean data type"""
        if not isinstance(self.value, bool):
            self.key_tree = self.key_tree if self.key_tree else self.key

            error_details[self.key_tree] = "Only allowed boolean data type."

        return error_details.get(self.key_tree)

    def case_predefined_constants(self):
        """Validate predefined constants"""
        if isinstance(self.value, str) and self.value in self.predefined_constants:
            ...
        else:
            self.key_tree = self.key_tree if self.key_tree else self.key

            error_details[
                self.key_tree] = (f"Chosen value is not in predefined"
                                  f" constants {tuple(self.predefined_constants)}.")

        return error_details.get(self.key_tree)

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
            self.key_tree = self.key_tree if self.key_tree else self.key

            error_details[self.key_tree] = "Only allowed data type is " + str(tuple(datatype_store))

        return error_details.get(self.key_tree)

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
