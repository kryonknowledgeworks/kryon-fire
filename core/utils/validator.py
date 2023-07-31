import re
from datetime import datetime

error_details = dict()


def case_regex(value, regex):
    if isinstance(value, str) and re.fullmatch(regex, value):
        return True


def format_change(datatype):
    if datatype in ["date", "dateTime"]:
        return "datetime"
    elif datatype == "boolean":
        return "bool"
    elif datatype == "string":
        return "str"
    elif datatype == "integer":
        return "int"


class DataTypeValidator:
    def __init__(self):
        self.predefinedConstants = None
        self.multi_datatype = None
        self.key = None
        self.regex = None
        self.value = None

    def initialize_datatype(self, datatype, value, key, regex=None, predefinedConstants=None, multi_datatype=None):
        default = "incorrect_datatype"
        self.value = value
        self.regex = regex
        self.key = key
        self.predefinedConstants = predefinedConstants
        self.multi_datatype = multi_datatype
        getattr(self, 'case_' + str(datatype), lambda: default)()

    def case_string(self):
        str_check = isinstance(self.value, str)

        if str_check:
            if self.regex:
                if case_regex(self.value, self.regex):
                    ...
                else:
                    error_details[self.key] = "Regex not matched."
        else:
            error_details[self.key] = "Only allowed string data type."

        return str_check

    def case_date(self):
        if isinstance(self.value, str) and re.fullmatch(self.regex, self.value):
            return True
        else:
            error_details[self.key] = "Invalid date format."

    def case_dateTime(self):
        if isinstance(self.value, str) and re.fullmatch(self.regex, self.value):
            return True
        else:
            error_details[self.key] = "Invalid date time format."

    def case_boolean(self):
        if isinstance(self.value, bool):
            return True
        else:
            error_details[self.key] = "Only allowed boolean data type."

    def case_predefinedConstants(self):
        if isinstance(self.value, str):
            if self.value in self.predefinedConstants:
                return True
            else:
                error_details[
                    self.key] = f"Chosen value is not in predefined constants {tuple(self.predefinedConstants)}."
        else:
            error_details[self.key] = "Only allowed string data type."

    def case_multi_datatype(self):
        from dateutil.parser import parse
        checklist = list()
        datatype_store = list()
        for multi_type in self.multi_datatype:
            datatype_store.append(multi_type.get("type"))
            if True not in checklist:
                if multi_type.get("type") in ["dateTime", "date"]:
                    try:
                        parse(self.value)
                        if isinstance(self.value, str) and re.fullmatch(multi_type.get("regex"), self.value):
                            checklist.append(True)
                    except ValueError:
                        checklist.append(False)
                elif multi_type.get("type") == "integer":
                    if isinstance(self.value, int):
                        checklist.append(True)
                    else:
                        checklist.append(False)
                elif multi_type.get("type") == "boolean":
                    if isinstance(self.value, bool):
                        checklist.append(True)
                    else:
                        checklist.append(False)
                elif multi_type.get("type") == "string":
                    if isinstance(self.value, str):
                        checklist.append(True)
                    else:
                        checklist.append(False)
        if True not in checklist:
            error_details[self.key] = "Only allowed data type is " + str(tuple(datatype_store))

    def validation_report(self):
        return error_details

    def reset_error_details(self):
        global error_details
        error_details = dict()
