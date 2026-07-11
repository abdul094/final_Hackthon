from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_secretsmanager as secretsmanager,
    CfnOutput,
)
from constructs import Construct


class Ec2PostgresStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.db_secret = secretsmanager.Secret(
            self, "PostgresDbSecret",
            secret_name="iot-postgres-credentials",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template='{"username": "iotadmin"}',
                generate_string_key="password",
                exclude_characters='"@/\\',
                password_length=16,
            ),
        )

        self.db_security_group = ec2.SecurityGroup(
            self, "PostgresSecurityGroup",
            vpc=vpc,
            description="Security group for PostgreSQL EC2 instance",
            allow_all_outbound=True,
        )
        self.db_security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4(vpc.vpc_cidr_block),
            connection=ec2.Port.tcp(5432),
            description="PostgreSQL access within VPC",
        )

        self.ec2_role = iam.Role(
            self, "PostgresEc2Role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")
            ],
        )
        self.db_secret.grant_read(self.ec2_role)

        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            "yum update -y",
            "amazon-linux-extras install postgresql14 -y || dnf install -y postgresql15 postgresql15-server",
            "postgresql-setup --initdb || /usr/bin/postgresql-setup --initdb",
            "systemctl enable postgresql",
            "systemctl start postgresql",
            "echo \"wal_level = logical\" >> /var/lib/pgsql/data/postgresql.conf",
            "echo \"host all all 0.0.0.0/0 md5\" >> /var/lib/pgsql/data/pg_hba.conf",
            "systemctl restart postgresql",
        )

        self.db_instance = ec2.Instance(
            self, "PostgresInstance",
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),
            machine_image=ec2.MachineImage.latest_amazon_linux2023(),
            security_group=self.db_security_group,
            role=self.ec2_role,
            user_data=user_data,
        )

        self.bastion = ec2.BastionHostLinux(
            self, "BastionHost",
            vpc=vpc,
            subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),
        )

        CfnOutput(self, "PostgresInstanceId", value=self.db_instance.instance_id)
        CfnOutput(self, "BastionInstanceId", value=self.bastion.instance_id)
        CfnOutput(self, "DbSecretName", value=self.db_secret.secret_name)