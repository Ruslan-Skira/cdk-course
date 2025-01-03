import aws_cdk as core
import aws_cdk.assertions as assertions
from aws_cdk.assertions import Match, Capture
import pytest

from py_testing.py_testing_stack import PyTestingStack


@pytest.fixture(scope="session")
def cdk_template():
    app = core.App()
    stack = PyTestingStack(app, "py-testing")
    template = assertions.Template.from_stack(stack)
    return template


def test_lambda_props(cdk_template):

    cdk_template.has_resource_properties("AWS::Lambda::Function", {"Runtime": "python3.12"})
    cdk_template.resource_count_is("AWS::Lambda::Function", 1)


def test_lambda_runtime_with_matcher(cdk_template):
    cdk_template.has_resource_properties("AWS::Lambda::Function", {"Runtime": Match.string_like_regexp("python")})


def test_lambda_policy_with_matcher(cdk_template):
    cdk_template.has_resource_properties(
        "AWS::IAM::Policy",
        Match.object_like(
            {
                "PolicyDocument": {
                    "Statement": [
                        {
                            "Resource": [
                                {
                                    "Fn::GetAtt": [
                                        Match.string_like_regexp("TestingBucket"),
                                        "Arn",
                                    ]
                                },
                                Match.any_value(),
                            ]
                        }
                    ]
                }
            }
        ),
    )


def test_lambda_actions_with_captors(cdk_template):
    lambda_action_captures = Capture()
    cdk_template.has_resource_properties(
        "AWS::IAM::Policy", {"PolicyDocument": {"Statement": [{"Action": lambda_action_captures}]}},
    )
    expected_actions = ["s3:GetBucket*", "s3:GetObject*", "s3:List*"]

    assert sorted(lambda_action_captures.as_array()) == sorted(expected_actions)
