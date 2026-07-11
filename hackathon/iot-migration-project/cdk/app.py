import aws_cdk as cdk
from stacks.vpc_stack import VpcStack
from stacks.msk_stack import MskStack
from stacks.ec2_postgres_stack import Ec2PostgresStack

app = cdk.App()
env = cdk.Environment(
    account="944508510066",
    region="us-east-1",
)
vpc_stack = VpcStack(app, "VpcStack", env=env)
msk_stack = MskStack(app, "MskStack", vpc=vpc_stack.vpc, env=env)
ec2_postgres_stack = Ec2PostgresStack(app, "Ec2PostgresStack", vpc=vpc_stack.vpc, env=env)
app.synth()