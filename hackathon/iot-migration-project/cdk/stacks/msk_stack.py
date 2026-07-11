from aws_cdk import (
    Stack,
    aws_msk as msk,
    aws_ec2 as ec2,
    CfnOutput,
)
from constructs import Construct


class MskStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.msk_security_group = ec2.SecurityGroup(
            self, "MskSecurityGroup",
            vpc=vpc,
            description="Security group for MSK Kafka cluster",
            allow_all_outbound=True,
        )

        self.msk_security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4(vpc.vpc_cidr_block),
            connection=ec2.Port.tcp(9092),
            description="Kafka plaintext",
        )
        self.msk_security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4(vpc.vpc_cidr_block),
            connection=ec2.Port.tcp(9094),
            description="Kafka TLS",
        )
        self.msk_security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4(vpc.vpc_cidr_block),
            connection=ec2.Port.tcp(2181),
            description="Zookeeper",
        )

        private_subnet_ids = [subnet.subnet_id for subnet in vpc.private_subnets]

        self.msk_cluster = msk.CfnCluster(
            self, "IotMskCluster",
            cluster_name="iot-events-cluster",
            kafka_version="3.5.1",
            number_of_broker_nodes=2,
            broker_node_group_info=msk.CfnCluster.BrokerNodeGroupInfoProperty(
                instance_type="kafka.t3.small",
                client_subnets=private_subnet_ids,
                security_groups=[self.msk_security_group.security_group_id],
                storage_info=msk.CfnCluster.StorageInfoProperty(
                    ebs_storage_info=msk.CfnCluster.EBSStorageInfoProperty(
                        volume_size=100
                    )
                ),
            ),
            encryption_info=msk.CfnCluster.EncryptionInfoProperty(
                encryption_in_transit=msk.CfnCluster.EncryptionInTransitProperty(
                    client_broker="TLS_PLAINTEXT",
                    in_cluster=True,
                )
            ),
        )

        CfnOutput(
            self, "MskClusterArn",
            value=self.msk_cluster.attr_arn,
            description="ARN of the MSK cluster",
        )