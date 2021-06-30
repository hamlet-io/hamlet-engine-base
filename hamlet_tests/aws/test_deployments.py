

# NOTE: this file must remain valid python file in order to perform tests on it


def cfn_lint_test(filename):
    import json
    import subprocess
    cmd = ' '.join([
        'cfn-lint',
        '-f',
        'json',
        filename
    ])
    result = subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf8'
    )
    if result.stderr:
        raise Exception(result.stderr)
    else:
        errors = json.loads(result.stdout)
        if errors:
            raise AssertionError(json.dumps(errors, indent=4))

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


# NOTE: This file must remain valid python file in order to perform tests on it.
# NOTE: Imports can't be used inside a template block because all code will be merged into a single file.
# NOTE: The class is wrapped into function in order to make it testable. This adds an ability to provide parent classes
# at runtime, otherwise, the module will raise NameError


def CFNStructure(JSONValidator):
    class CFNStructure(JSONValidator):

        RESOURCES_KEY = 'Resources'
        RESOURCE_TYPE_KEY = 'Type'
        OUTPUT_KEY = 'Outputs'

        def __resource(self, id, type):
            def validator():
                resources = self._body.get(self.RESOURCES_KEY, {})
                target = resources.get(id)
                assert target is not None, 'cfn resource {} is missing'.format(id)
                assert target[self.RESOURCE_TYPE_KEY] == type, 'cfn resource {}.{}!={}'.format(
                    id,
                    self.RESOURCE_TYPE_KEY,
                    type
                )
            validator.__name__ = 'cfn resource {}.{} == {}'.format(id, self.RESOURCE_TYPE_KEY, type)
            return validator

        def __output(self, id):
            def validator():
                output = self._body.get(self.OUTPUT_KEY, {})
                value = output.get(id)
                assert value is not None, 'cfn output {} is missing'.format(id)
            validator.__name__ = 'cfn output {} exists'.format(id)
            return validator

        def resource(self, id, type):
            self._validators.append(self.__resource(id, type))
            return self

        def output(self, id):
            self._validators.append(self.__output(id))
            return self
    return CFNStructure


CFNStructure = CFNStructure(JSONValidator)



# *****************************************************************************
# * TESTCASE aws_apigateway_base_app_apigatewaybase_apigateway_apigatewaybase *
# *****************************************************************************
def test_aws_apigateway_base_app_apigatewaybase_apigateway_apigatewaybase():
    filename = "app-aws-apigateway-base-ap-southeast-2-template.json"

    cfn_structure = CFNStructure.from_file(filename)

    cfn_structure.resource("apiXappXapigatewaybase", "AWS::ApiGateway::RestApi")
    cfn_structure.resource("apiDeployXappXapigatewaybaseXrunId098", "AWS::ApiGateway::Deployment")


    cfn_structure.output("apiXappXapigatewaybase")
    cfn_structure.output("apiXappXapigatewaybaseXroot")
    cfn_structure.output("apiXappXapigatewaybaseXregion")

    cfn_structure.assert_structure()



# ******************************************************************
# * TESTCASE aws_bastion_base_mgmt_bastionbase_bastion_bastionbase *
# ******************************************************************
def test_aws_bastion_base_mgmt_bastionbase_bastion_bastionbase():
    filename = "seg-aws-bastion-base-ap-southeast-2-template.json"

    cfn_lint_test(filename)

    json_structure = JSONStructure.from_file(filename)

    json_structure.match("Resources.asgXmgmtXbastionbase.UpdatePolicy.AutoScalingRollingUpdate.WaitOnResourceSignals", True)
    json_structure.match("Resources.asgXmgmtXbastionbase.Properties.DesiredCapacity", "0")
    json_structure.match("Resources.securityGroupXmgmtXbastionbase.Properties.VpcId", "##MockOutputXvpcXsegmentXvpcX##")

    json_structure.not_empty("Resources.launchConfigXmgmtXbastionbase.Properties.ImageId")
    json_structure.not_empty("Resources.launchConfigXmgmtXbastionbase.Properties.InstanceType")
    json_structure.not_empty("Resources.asgXmgmtXbastionbase.Metadata")

    json_structure.assert_structure()

    cfn_structure = CFNStructure.from_file(filename)

    cfn_structure.resource("launchConfigXmgmtXbastionbase", "AWS::AutoScaling::LaunchConfiguration")
    cfn_structure.resource("securityGroupXmgmtXbastionbase", "AWS::EC2::SecurityGroup")
    cfn_structure.resource("asgXmgmtXbastionbase", "AWS::AutoScaling::AutoScalingGroup")


    cfn_structure.output("securityGroupXmgmtXbastionbase")
    cfn_structure.output("asgXmgmtXbastionbase")

    cfn_structure.assert_structure()



# *********************************************************************************************
# * TESTCASE aws_computecluster_base_app_computeclusterbase_computecluster_computeclusterbase *
# *********************************************************************************************
def test_aws_computecluster_base_app_computeclusterbase_computecluster_computeclusterbase():
    filename = "app-aws-computecluster-base-ap-southeast-2-template.json"

    cfn_lint_test(filename)

    json_structure = JSONStructure.from_file(filename)

    json_structure.not_empty("Resources.launchConfigXappXcomputeclusterbaseXHamletFatalBuildreferencenotfound.Properties.ImageId")
    json_structure.not_empty("Resources.launchConfigXappXcomputeclusterbaseXHamletFatalBuildreferencenotfound.Properties.InstanceType")
    json_structure.not_empty("Resources.launchConfigXappXcomputeclusterbaseXHamletFatalBuildreferencenotfound.Properties.UserData")
    json_structure.not_empty("Resources.asgXappXcomputeclusterbase.Metadata")

    json_structure.assert_structure()

    cfn_structure = CFNStructure.from_file(filename)

    cfn_structure.resource("securityGroupXappXcomputeclusterbase", "AWS::EC2::SecurityGroup")
    cfn_structure.resource("asgXappXcomputeclusterbase", "AWS::AutoScaling::AutoScalingGroup")


    cfn_structure.output("asgXappXcomputeclusterbase")
    cfn_structure.output("securityGroupXappXcomputeclusterbase")

    cfn_structure.assert_structure()



# ****************************************************************************************
# * TESTCASE aws_datapipeline_base_app_datapipelinebase_datapipeline_datapipelinebasecli *
# ****************************************************************************************
def test_aws_datapipeline_base_app_datapipelinebase_datapipeline_datapipelinebasecli():
    filename = "app-aws-datapipeline-base-ap-southeast-2-cli.json"

    json_structure = JSONStructure.from_file(filename)

    json_structure.match("datapipelineXappXdatapipelinebase.createPipeline.name", "mockedup-integration-application-datapipelinebase")
    json_structure.match("datapipelineXappXdatapipelinebase.createPipeline.uniqueId", "datapipelineXappXdatapipelinebase")

    json_structure.assert_structure()



# *******************************************************************************************
# * TESTCASE aws_datapipeline_base_app_datapipelinebase_datapipeline_datapipelinebaseconfig *
# *******************************************************************************************
def test_aws_datapipeline_base_app_datapipelinebase_datapipeline_datapipelinebaseconfig():
    filename = "app-aws-datapipeline-base-ap-southeast-2-config.json"

    json_structure = JSONStructure.from_file(filename)

    json_structure.match("values.my_VPC_ID", "##MockOutputXvpcXsegmentXvpcX##")
    json_structure.match("values.my_ROLE_PIPELINE_NAME", "mockedup-integration-application-datapipelinebase-pipeline")

    json_structure.assert_structure()



# *********************************************************************************************
# * TESTCASE aws_datapipeline_base_app_datapipelinebase_datapipeline_datapipelinebasetemplate *
# *********************************************************************************************
def test_aws_datapipeline_base_app_datapipelinebase_datapipeline_datapipelinebasetemplate():
    filename = "app-aws-datapipeline-base-ap-southeast-2-template.json"

    cfn_structure = CFNStructure.from_file(filename)

    cfn_structure.resource("instanceProfileXappXdatapipelinebase", "AWS::IAM::InstanceProfile")
    cfn_structure.resource("securityGroupXappXdatapipelinebase", "AWS::EC2::SecurityGroup")


    cfn_structure.output("securityGroupXappXdatapipelinebase")

    cfn_structure.assert_structure()



# *********************************************************************
# * TESTCASE aws_db_postgres_base_db_postgresdbbase_db_postgresdbbase *
# *********************************************************************
def test_aws_db_postgres_base_db_postgresdbbase_db_postgresdbbase():
    filename = "soln-aws-db-postgres-base-ap-southeast-2-template.json"

    json_structure = JSONStructure.from_file(filename)

    json_structure.match("Resources.rdsXdbXpostgresdbbase.Properties.Engine", "postgres")
    json_structure.match("Resources.rdsXdbXpostgresdbbase.Properties.EngineVersion", "11")
    json_structure.match("Resources.rdsOptionGroupXdbXpostgresdbbaseXpostgres11.Properties.MajorEngineVersion", "11")
    json_structure.match("Resources.rdsParameterGroupXdbXpostgresdbbaseXpostgres11.Properties.Family", "postgres11")

    json_structure.not_empty("Resources.rdsXdbXpostgresdbbase.Properties.DBInstanceClass")

    json_structure.assert_structure()

    cfn_structure = CFNStructure.from_file(filename)

    cfn_structure.resource("rdsXdbXpostgresdbbase", "AWS::RDS::DBInstance")
    cfn_structure.resource("rdsOptionGroupXdbXpostgresdbbaseXpostgres11", "AWS::RDS::OptionGroup")
    cfn_structure.resource("rdsParameterGroupXdbXpostgresdbbaseXpostgres11", "AWS::RDS::DBParameterGroup")


    cfn_structure.output("rdsXdbXpostgresdbbaseXdns")
    cfn_structure.output("rdsXdbXpostgresdbbaseXport")
    cfn_structure.output("securityGroupXdbXpostgresdbbase")

    cfn_structure.assert_structure()



# ************************************************************************************
# * TESTCASE aws_db_postgres_generated_db_postgresdbgenerated_db_postgresdbgenerated *
# ************************************************************************************
def test_aws_db_postgres_generated_db_postgresdbgenerated_db_postgresdbgenerated():
    filename = "soln-aws-db-postgres-generated-ap-southeast-2-template.json"

    cfn_structure = CFNStructure.from_file(filename)

    cfn_structure.resource("rdsXdbXpostgresdbgenerated", "AWS::RDS::DBInstance")


    cfn_structure.output("rdsXdbXpostgresdbgeneratedXdns")
    cfn_structure.output("rdsXdbXpostgresdbgeneratedXport")

    cfn_structure.assert_structure()



# *************************************************
# * TESTCASE aws_ec2_base_app_ec2base_ec2_ec2base *
# *************************************************
def test_aws_ec2_base_app_ec2base_ec2_ec2base():
    filename = "soln-aws-ec2-base-ap-southeast-2-template.json"

    cfn_lint_test(filename)

    json_structure = JSONStructure.from_file(filename)

    json_structure.match("Resources.ec2InstanceXappXec2baseXa.Properties.NetworkInterfaces[0].NetworkInterfaceId", "##MockOutputXeniXappXec2baseXaXeth0X##")
    json_structure.match("Resources.eniXappXec2baseXaXeth0.Properties.SubnetId", "##MockOutputXsubnetXappXaX##")

    json_structure.not_empty("Resources.ec2InstanceXappXec2baseXa.Properties.ImageId")
    json_structure.not_empty("Resources.ec2InstanceXappXec2baseXa.Properties.InstanceType")
    json_structure.not_empty("Resources.ec2InstanceXappXec2baseXa.Metadata")

    json_structure.assert_structure()

    cfn_structure = CFNStructure.from_file(filename)

    cfn_structure.resource("securityGroupXappXec2base", "AWS::EC2::SecurityGroup")
    cfn_structure.resource("ec2InstanceXappXec2baseXa", "AWS::EC2::Instance")
    cfn_structure.resource("eniXappXec2baseXaXeth0", "AWS::EC2::NetworkInterface")


    cfn_structure.output("securityGroupXappXec2base")

    cfn_structure.assert_structure()



# *************************************************
# * TESTCASE aws_ecs_base_app_ecsbase_ecs_ecsbase *
# *************************************************
def test_aws_ecs_base_app_ecsbase_ecs_ecsbase():
    filename = "soln-aws-ecs-base-ap-southeast-2-template.json"

    cfn_lint_test(filename)

    json_structure = JSONStructure.from_file(filename)

    json_structure.match("Resources.asgXappXecsbase.UpdatePolicy.AutoScalingRollingUpdate.WaitOnResourceSignals", True)
    json_structure.match("Resources.securityGroupXappXecsbase.Properties.VpcId", "##MockOutputXvpcXsegmentXvpcX##")
    json_structure.match("Resources.ecsCapacityProviderAssocXappXecsbase.Properties.CapacityProviders", ['FARGATE', 'FARGATE_SPOT', '##MockOutputXecsCapacityProviderXappXecsbaseXasgX##'])

    json_structure.not_empty("Resources.launchConfigXappXecsbase.Properties.ImageId")
    json_structure.not_empty("Resources.launchConfigXappXecsbase.Properties.InstanceType")
    json_structure.not_empty("Resources.asgXappXecsbase.Metadata")

    json_structure.assert_structure()

    cfn_structure = CFNStructure.from_file(filename)

    cfn_structure.resource("launchConfigXappXecsbase", "AWS::AutoScaling::LaunchConfiguration")
    cfn_structure.resource("securityGroupXappXecsbase", "AWS::EC2::SecurityGroup")
    cfn_structure.resource("asgXappXecsbase", "AWS::AutoScaling::AutoScalingGroup")
    cfn_structure.resource("ecsXappXecsbase", "AWS::ECS::Cluster")
    cfn_structure.resource("ecsCapacityProviderXappXecsbaseXasg", "AWS::ECS::CapacityProvider")


    cfn_structure.output("securityGroupXappXecsbase")
    cfn_structure.output("asgXappXecsbase")
    cfn_structure.output("ecsXappXecsbase")
    cfn_structure.output("ecsXappXecsbaseXarn")

    cfn_structure.assert_structure()



# *************************************************************************************
# * TESTCASE aws_filetransfer_base_app_filetransferbase_filetransfer_filetransferbase *
# *************************************************************************************
def test_aws_filetransfer_base_app_filetransferbase_filetransfer_filetransferbase():
    filename = "soln-aws-filetransfer-base-ap-southeast-2-template.json"

    cfn_structure = CFNStructure.from_file(filename)

    cfn_structure.resource("transferServerXappXfiletransferbase", "AWS::Transfer::Server")
    cfn_structure.resource("securityGroupXtransferServerXappXfiletransferbase", "AWS::EC2::SecurityGroup")


    cfn_structure.output("transferServerXappXfiletransferbase")
    cfn_structure.output("transferServerXappXfiletransferbaseXarn")
    cfn_structure.output("transferServerXappXfiletransferbaseXname")

    cfn_structure.assert_structure()



# *******************************************************************************************************
# * TESTCASE aws_healthcheck_complex_base_app_healthcheckcomplexbase_healthcheck_healthcheckcomplexbase *
# *******************************************************************************************************
def test_aws_healthcheck_complex_base_app_healthcheckcomplexbase_healthcheck_healthcheckcomplexbase():
    filename = "app-aws-healthcheck-complex-base-ap-southeast-2-template.json"

    cfn_lint_test(filename)

    json_structure = JSONStructure.from_file(filename)

    json_structure.match("Resources.canaryXappXhealthcheckcomplexbase.Properties.Name", "healthcheckcomplexbas")
    json_structure.match("Resources.canaryXappXhealthcheckcomplexbase.Properties.ArtifactS3Location", "s3://##MockOutputXs3XsegmentXapplicationX##/appdata/mockedup/integration/application/healthcheckcomplexbase")
    json_structure.match("Resources.canaryXappXhealthcheckcomplexbase.Properties.RunConfig.EnvironmentVariables.LB_FQDN", "healthchecklb-integration.mock.local")

    json_structure.assert_structure()

    cfn_structure = CFNStructure.from_file(filename)

    cfn_structure.resource("canaryXappXhealthcheckcomplexbase", "AWS::Synthetics::Canary")


    cfn_structure.output("canaryXappXhealthcheckcomplexbase")

    cfn_structure.assert_structure()



# ****************************************************
# * TESTCASE aws_lb_app_https_elb_httpslb_lb_httpslb *
# ****************************************************
def test_aws_lb_app_https_elb_httpslb_lb_httpslb():
    filename = "soln-aws-lb-app-https-ap-southeast-2-template.json"

    json_structure = JSONStructure.from_file(filename)

    json_structure.match("Resources.albXelbXhttpslb.Properties.Name", "mockedup-int-elb-httpslb")
    json_structure.match("Resources.listenerRuleXelbXhttpslbXhttpX100.Properties.Actions[0]", {'Type': 'redirect', 'RedirectConfig': {'Path': '/#{path}', 'Query': '#{query}', 'Port': '443', 'Host': '#{host}', 'Protocol': 'HTTPS', 'StatusCode': 'HTTP_301'}})
    json_structure.match("Resources.listenerRuleXelbXhttpslbXhttpsX500.Properties.Actions[0].Type", "forward")

    json_structure.not_empty("Resources.listenerRuleXelbXhttpslbXhttpX100.Properties.Priority")

    json_structure.len("Resources.listenerRuleXelbXhttpslbXhttpX100.Properties.Actions", 1)

    json_structure.assert_structure()

    cfn_structure = CFNStructure.from_file(filename)

    cfn_structure.resource("listenerRuleXelbXhttpslbXhttpX100", "AWS::ElasticLoadBalancingV2::ListenerRule")
    cfn_structure.resource("listenerXelbXhttpslbXhttps", "AWS::ElasticLoadBalancingV2::Listener")
    cfn_structure.resource("albXelbXhttpslb", "AWS::ElasticLoadBalancingV2::LoadBalancer")


    cfn_structure.output("securityGroupXlistenerXelbXhttpslbXhttps")
    cfn_structure.output("listenerRuleXelbXhttpslbXhttpsX500")
    cfn_structure.output("tgXdefaultXelbXhttpslbXhttps")

    cfn_structure.assert_structure()



# *******************************************************
# * TESTCASE aws_lb_app_https_elb_httpslb_lb_validation *
# *******************************************************
def test_aws_lb_app_https_elb_httpslb_lb_validation():
    filename = "soln-aws-lb-app-https-ap-southeast-2-template.json"

    cfn_lint_test(filename)



# *************************************************************************
# * TESTCASE aws_mobileapp_base_app_mobileappbase_mobileapp_mobileappbase *
# *************************************************************************
def test_aws_mobileapp_base_app_mobileappbase_mobileapp_mobileappbase():
    filename = "app-aws-mobileapp-base-ap-southeast-2-config.json"

    json_structure = JSONStructure.from_file(filename)

    json_structure.match("BuildConfig.APP_BUILD_FORMATS", "ios,android")
    json_structure.match("BuildConfig.BUILD_REFERENCE]", "123456789#MockCommit#")
    json_structure.match("BuildConfig.RELEASE_CHANNEL", "integration")

    json_structure.assert_structure()



# *************************************************************************
# * TESTCASE aws_queuehost_base_app_queuehostbase_queuehost_queuehostbase *
# *************************************************************************
def test_aws_queuehost_base_app_queuehostbase_queuehost_queuehostbase():
    filename = "soln-aws-queuehost-base-ap-southeast-2-template.json"

    cfn_structure = CFNStructure.from_file(filename)

    cfn_structure.resource("mqBrokerXappXqueuehostbase", "AWS::AmazonMQ::Broker")
    cfn_structure.resource("securityGroupXmqBrokerXappXqueuehostbase", "AWS::EC2::SecurityGroup")
    cfn_structure.resource("secretXappXqueuehostbaseXroot", "AWS::SecretsManager::Secret")


    cfn_structure.output("mqBrokerXappXqueuehostbaseXdns")
    cfn_structure.output("securityGroupXmqBrokerXappXqueuehostbase")
    cfn_structure.output("secretXappXqueuehostbaseXroot")

    cfn_structure.assert_structure()



# *********************************************
# * TESTCASE aws_s3_base_app_s3base_s3_s3base *
# *********************************************
def test_aws_s3_base_app_s3base_s3_s3base():
    filename = "soln-aws-s3-base-ap-southeast-2-template.json"

    cfn_structure = CFNStructure.from_file(filename)

    cfn_structure.resource("s3XappXs3base", "AWS::S3::Bucket")


    cfn_structure.output("s3XappXs3base")
    cfn_structure.output("s3XappXs3baseXname")
    cfn_structure.output("s3XappXs3baseXarn")
    cfn_structure.output("s3XappXs3baseXregion")

    cfn_structure.assert_structure()



# ***************************************************
# * TESTCASE aws_s3_notify_app_s3notify_s3_s3notify *
# ***************************************************
def test_aws_s3_notify_app_s3notify_s3_s3notify():
    filename = "soln-aws-s3-notify-ap-southeast-2-template.json"

    json_structure = JSONStructure.from_file(filename)

    json_structure.match("Resources.s3XappXs3notify.Properties.NotificationConfiguration.QueueConfigurations[0].Queue", "arn:aws:iam::123456789012:mock/sqsXappXs3notifyqueueXarn")

    json_structure.assert_structure()

    cfn_structure = CFNStructure.from_file(filename)

    cfn_structure.resource("s3XappXs3notify", "AWS::S3::Bucket")
    cfn_structure.resource("sqsXappXs3notifyqueue", "AWS::SQS::Queue")
    cfn_structure.resource("sqsPolicyXappXs3notifyqueue", "AWS::SQS::QueuePolicy")


    cfn_structure.output("s3XappXs3notify")
    cfn_structure.output("s3XappXs3notifyXname")
    cfn_structure.output("s3XappXs3notifyXarn")
    cfn_structure.output("s3XappXs3notifyXregion")

    cfn_structure.assert_structure()



# *************************************************************
# * TESTCASE aws_s3_replication_app_s3replicasrc_s3_s3replica *
# *************************************************************
def test_aws_s3_replication_app_s3replicasrc_s3_s3replica():
    filename = "soln-aws-s3-replication-ap-southeast-2-template.json"

    json_structure = JSONStructure.from_file(filename)

    json_structure.match("Resources.s3XappXs3replicasrc.Properties.ReplicationConfiguration.Rules[0].Destination.Bucket", "arn:aws:iam::123456789012:mock/s3XappXs3replicadstXarn")

    json_structure.assert_structure()

    cfn_structure = CFNStructure.from_file(filename)

    cfn_structure.resource("s3XappXs3replicasrc", "AWS::S3::Bucket")
    cfn_structure.resource("s3XappXs3replicadst", "AWS::S3::Bucket")


    cfn_structure.output("s3XappXs3replicasrc")
    cfn_structure.output("s3XappXs3replicasrcXname")
    cfn_structure.output("s3XappXs3replicasrcXarn")
    cfn_structure.output("s3XappXs3replicasrcXregion")
    cfn_structure.output("s3XappXs3replicadst")
    cfn_structure.output("s3XappXs3replicadstXname")
    cfn_structure.output("s3XappXs3replicadstXarn")
    cfn_structure.output("s3XappXs3replicadstXregion")

    cfn_structure.assert_structure()



# ****************************************************************************
# * TESTCASE aws_s3_replication_external_app_s3replicasextrc_s3_s3replicaext *
# ****************************************************************************
def test_aws_s3_replication_external_app_s3replicasextrc_s3_s3replicaext():
    filename = "soln-aws-s3-replication-external-ap-southeast-2-template.json"

    json_structure = JSONStructure.from_file(filename)

    json_structure.match("Resources.s3XappXs3replicasextrc.Properties.ReplicationConfiguration.Rules[0].Destination.Bucket", "arn:aws:s3:::external-replication-destination")
    json_structure.match("Resources.s3XappXs3replicasextrc.Properties.ReplicationConfiguration.Rules[0].Destination.AccessControlTranslation.Owner", "Destination")
    json_structure.match("Resources.s3XappXs3replicasextrc.Properties.ReplicationConfiguration.Rules[0].Destination.Account", "0987654321")

    json_structure.assert_structure()

    cfn_structure = CFNStructure.from_file(filename)

    cfn_structure.resource("s3XappXs3replicasextrc", "AWS::S3::Bucket")


    cfn_structure.output("s3XappXs3replicasextrc")
    cfn_structure.output("s3XappXs3replicasextrcXname")
    cfn_structure.output("s3XappXs3replicasextrcXarn")
    cfn_structure.output("s3XappXs3replicasextrcXregion")

    cfn_structure.assert_structure()
