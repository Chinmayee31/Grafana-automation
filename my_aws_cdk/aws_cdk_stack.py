from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    Stack
)
from constructs import Construct 

class Ec2WindowsInstanceStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a VPC
        vpc = ec2.Vpc(
            self, "MyVpc",
            max_azs=2 , # Default is all AZs in the region
            nat_gateways=0  # this is to ensure there's public subnet
        )

        # Use an existing AMI ID for Windows
        my_ami = ec2.MachineImage.generic_windows({
            "eu-central-1": "ami-018dbdf8abb7619e2"  # Replace 
        })

        #  Security Group 
        security_group = ec2.SecurityGroup(
            self, "MySecurityGroup",
            vpc=vpc,
            security_group_name="AllowRDP",
            description="Allow RDP access to Windows instance",
            allow_all_outbound=True
        )

        # Allow inbound traffic on port 3389 (RDP)
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(3389),
            "Allow RDP from anywhere"
        )
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(3000),
            "Allow access to application on port 3000"
        )

        # Create an EC2 instance using the specific AMI
        instance = ec2.Instance(
            self, "WindowsInstance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=my_ami,
            vpc=vpc,
            security_group=security_group,
            key_name="Grafana", # Replace with your key pair name
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC  # Ensure the instance is in a public subnet
            )
        )

        
