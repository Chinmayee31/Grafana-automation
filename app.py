#!/usr/bin/env python3
import aws_cdk as cdk
from my_aws_cdk.aws_cdk_stack import Ec2WindowsInstanceStack

app = cdk.App()
Ec2WindowsInstanceStack(app, "Ec2WindowsInstanceStack")

app.synth()
