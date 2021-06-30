

class JSONValidator:
    def __init__(self, body):
        self._body = body
        self._validators = []

    @classmethod
    def from_file(cls, filename):
        try:
            with open(filename, "rt") as f:
                import json
                return cls(json.load(f))
        except FileNotFoundError as e:
            raise AssertionError("%s not found" % filename) from e
        except ValueError as e:
            raise AssertionError("%s is not a valid JSON" % filename) from e

    @staticmethod
    def _split_path(path):
        import re
        keys = []
        for m in re.finditer(r"(\w+)|\[(\d+)\]", path):
            key = m.group(1)
            index = m.group(2)
            if key is not None:
                keys.append(key)
            elif index is not None:
                keys.append(int(index))
        return keys

    @staticmethod
    def _format_keys_to_path(keys):
        result = ""
        for key in keys:
            if isinstance(key, int):
                result += "[%s]" % key
            else:
                result += ".%s" % key
        if result.startswith('.'):
            result = result[1:]
        return result

    def _get_value_by_json_path(self, path):
        keys = self._split_path(path)
        traversed_keys = []
        value = self._body
        for key in keys:
            traversed_keys.append(key)
            try:
                value = value[key]
            except (KeyError, IndexError) as e:
                raise AssertionError('{} does not exist'.format(self._format_keys_to_path(traversed_keys))) from e
        return value

    @property
    def errors(self):
        try:
            return self._errors
        except AttributeError:
            errors = []
            for validator in self._validators:
                try:
                    validator()
                except AssertionError as e:
                    msg = None
                    if e.args:
                        msg = e.args[0].split('\n')[0]
                    errors.append(
                        {
                            'rule': validator.__name__,
                            'msg': msg
                        }
                    )
            self._errors = errors
            return errors

    def assert_structure(self):
        import json
        if self.errors:
            raise AssertionError(json.dumps(self.errors, indent=4))


# NOTE: This file must remain valid python file in order to perform tests on it.
# NOTE: Imports can't be used inside a template block because all code will be merged into a single file.
# NOTE: The class is wrapped into function in order to make it testable. This adds an ability to provide parent classes
# at runtime, otherwise, the module will raise NameError


def JSONStructure(JSONValidator):
    class JSONStructure(JSONValidator):

        def __match(self, path, target):
            def validator():
                value = self._get_value_by_json_path(path)
                assert value == target, '{} doesn\'t match {}'.format(path, target)
            validator.__name__ = '{} == {}'.format(path, target)
            return validator

        def __len(self, path, target):
            def validator():
                value = self._get_value_by_json_path(path)
                assert len(value) == target, '{}.length={}!={}'.format(path, len(value), target)
            validator.__name__ = '{}.length == {}'.format(path, target)
            return validator

        def __exists(self, path):
            def validator():
                return self._get_value_by_json_path(path)
            validator.__name__ = '{} exists?'.format(path)
            return validator

        def __not_empty(self, path):
            def validator():
                value = self._get_value_by_json_path(path)
                assert_text = '{} is empty'.format(path)
                assert value is not None, assert_text
                if isinstance(value, (str, dict, list)):
                    assert len(value) > 0, assert_text
            validator.__name__ = 'not empty {}?'.format(path)
            return validator

        def match(self, path, target):
            self._validators.append(self.__match(path, target))
            return self

        def len(self, path, target):
            self._validators.append(self.__len(path, target))
            return self

        def exists(self, path):
            self._validators.append(self.__exists(path))
            return self

        def not_empty(self, path):
            self._validators.append(self.__not_empty(path))
            return self
    return JSONStructure


JSONStructure = JSONStructure(JSONValidator)



# ************************************************************************
# * TESTCASE shared_contextpath_app_contextpath_internaltest_contextpath *
# ************************************************************************
def test_shared_contextpath_app_contextpath_internaltest_contextpath():
    filename = "deployment-internal-shared-contextpath-mock-region-1-config.json"

    json_structure = JSONStructure.from_file(filename)

    json_structure.match("Occurrence.State.Attributes.ALLINCLUDES_CONTEXTPATH_OUTPUT", "mockacct-0123456789-mockedup-mockapp-integration-default-application-contextpath-allincludes")

    json_structure.assert_structure()



# *********************************************************************************************
# * TESTCASE shared_internaltest_base_app_internaltestbase_internaltest_internaltestbase_core *
# *********************************************************************************************
def test_shared_internaltest_base_app_internaltestbase_internaltest_internaltestbase_core():
    filename = "deployment-internal-shared-internaltest-base-mock-region-1-config.json"

    json_structure = JSONStructure.from_file(filename)

    json_structure.match("Occurrence.Core.Id", "appXinternaltestbase")
    json_structure.match("Occurrence.Core.Name", "application-internaltestbase")
    json_structure.match("Occurrence.Core.FullName", "mockedup-integration-application-internaltestbase")
    json_structure.match("Occurrence.Core.RelativePath", "application/internaltestbase")
    json_structure.match("Occurrence.Core.FullAbsolutePath", "/mockedup/integration/application/internaltestbase")

    json_structure.assert_structure()
