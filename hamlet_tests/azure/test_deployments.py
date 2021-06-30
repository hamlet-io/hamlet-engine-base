

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



# ********************************************************************************************
# * TESTCASE application_az_apigateway_base_api_apigateway_apigateway_baseapigatewaytemplate *
# ********************************************************************************************
def test_application_az_apigateway_base_api_apigateway_apigateway_baseapigatewaytemplate():
    filename = "app-application-az-apigateway-base-westus-template.json"

    json_structure = JSONStructure.from_file(filename)

    json_structure.match("outputs.serviceXmockedupXintegrationXapiXapigateway.value", "/subscriptions/0123456789/resourceGroups/mockRG/providers/Microsoft.Mock/mockResourceType/mockName")

    json_structure.assert_structure()



# ************************************************************************************************************
# * TESTCASE application_az_computecluster_base_app_computecluster_computecluster_basecomputeclustertemplate *
# ************************************************************************************************************
def test_application_az_computecluster_base_app_computecluster_computecluster_basecomputeclustertemplate():
    filename = "app-application-az-computecluster-base-westus-template.json"

    json_structure = JSONStructure.from_file(filename)

    json_structure.match("outputs.vmssXsettingsXappXcomputecluster.value", "/subscriptions/0123456789/resourceGroups/mockRG/providers/Microsoft.Mock/mockResourceType/mockName")

    json_structure.assert_structure()



# ****************************************************************************
# * TESTCASE application_az_lambda_base_app_lambda_lambda_baselambdatemplate *
# ****************************************************************************
def test_application_az_lambda_base_app_lambda_lambda_baselambdatemplate():
    filename = "app-application-az-lambda-base-westus-template.json"

    json_structure = JSONStructure.from_file(filename)

    json_structure.match("outputs.sitesXappXlambdaXapi.value", "/subscriptions/0123456789/resourceGroups/mockRG/providers/Microsoft.Mock/mockResourceType/mockName")

    json_structure.assert_structure()



# ****************************************************************
# * TESTCASE application_az_spa_base_app_spa_spa_basespatemplate *
# ****************************************************************
def test_application_az_spa_base_app_spa_spa_basespatemplate():
    filename = "app-application-az-spa-base-westus-config.json"

    json_structure = JSONStructure.from_file(filename)

    json_structure.exists("RUN_ID")

    json_structure.assert_structure()



# *****************************************************************
# * TESTCASE baseline_mgmt_baseline_baseline_basebaselinetemplate *
# *****************************************************************
def test_baseline_mgmt_baseline_baseline_basebaselinetemplate():
    filename = "seg-baseline-westus-template.json"

    json_structure = JSONStructure.from_file(filename)

    json_structure.match("outputs.storageXmgmtXbaseline.value", "/subscriptions/0123456789/resourceGroups/mockRG/providers/Microsoft.Mock/mockResourceType/mockName")

    json_structure.assert_structure()



# *****************************************************************************
# * TESTCASE segment_az_bastion_base_mgmt_bastion_bastion_basebastiontemplate *
# *****************************************************************************
def test_segment_az_bastion_base_mgmt_bastion_bastion_basebastiontemplate():
    filename = "seg-segment-az-bastion-base-westus-template.json"

    json_structure = JSONStructure.from_file(filename)

    json_structure.match("outputs.vmssXmanagementXbastionXbastion.value", "/subscriptions/0123456789/resourceGroups/mockRG/providers/Microsoft.Mock/mockResourceType/mockName")

    json_structure.assert_structure()



# **************************************************************************
# * TESTCASE segment_az_network_base_mgmt_vnet_network_basenetworktemplate *
# **************************************************************************
def test_segment_az_network_base_mgmt_vnet_network_basenetworktemplate():
    filename = "seg-segment-az-network-base-westus-template.json"

    json_structure = JSONStructure.from_file(filename)

    json_structure.match("outputs.vnetXmgmtXvnet.value", "/subscriptions/0123456789/resourceGroups/mockRG/providers/Microsoft.Mock/mockResourceType/mockName")

    json_structure.assert_structure()



# *************************************************************
# * TESTCASE solution_az_cdn_base_web_cdn_cdn_basecdntemplate *
# *************************************************************
def test_solution_az_cdn_base_web_cdn_cdn_basecdntemplate():
    filename = "soln-solution-az-cdn-base-westus-template.json"

    json_structure = JSONStructure.from_file(filename)

    json_structure.match("outputs.frontdoorXwebXcdn.value", "/subscriptions/0123456789/resourceGroups/mockRG/providers/Microsoft.Mock/mockResourceType/mockName")

    json_structure.assert_structure()



# **************************************************************
# * TESTCASE solution_az_db_base_db_database_db_basedbtemplate *
# **************************************************************
def test_solution_az_db_base_db_database_db_basedbtemplate():
    filename = "soln-solution-az-db-base-westus-template.json"

    json_structure = JSONStructure.from_file(filename)

    json_structure.match("outputs.postgresserverXdbXdatabaseXurl.value", "https://mock.local/postgresserverXdbXdatabaseXurl")

    json_structure.assert_structure()



# *********************************************************
# * TESTCASE solution_az_lb_base_elb_lb_lb_baselbtemplate *
# *********************************************************
def test_solution_az_lb_base_elb_lb_lb_baselbtemplate():
    filename = "soln-solution-az-lb-base-westus-template.json"

    json_structure = JSONStructure.from_file(filename)

    json_structure.match("outputs.appGatewayXmockedupXintegrationXelbXlb.value", "/subscriptions/0123456789/resourceGroups/mockRG/providers/Microsoft.Mock/mockResourceType/mockName")

    json_structure.assert_structure()



# **************************************************************
# * TESTCASE solution_az_mysqldb_db_mysqldb_db_mysqldbtemplate *
# **************************************************************
def test_solution_az_mysqldb_db_mysqldb_db_mysqldbtemplate():
    filename = "soln-solution-az-mysqldb-westus-template.json"

    json_structure = JSONStructure.from_file(filename)

    json_structure.match("outputs.mysqlserverXdbXmysqldbXurl.value", "https://mock.local/mysqlserverXdbXmysqldbXurl")

    json_structure.assert_structure()



# ************************************************************
# * TESTCASE solution_az_s3_base_app_stage_s3_bases3template *
# ************************************************************
def test_solution_az_s3_base_app_stage_s3_bases3template():
    filename = "soln-solution-az-s3-base-westus-template.json"

    json_structure = JSONStructure.from_file(filename)

    json_structure.match("outputs.storageXappXstage.value", "/subscriptions/0123456789/resourceGroups/mockRG/providers/Microsoft.Mock/mockResourceType/mockName")

    json_structure.assert_structure()
