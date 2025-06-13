#!/usr/bin/env python3
import aws_cdk as cdk
from infra.messaging_stack import MessagingStack
from infra.persistence_stack import PersistenceStack
from infra.compute_stack import ComputeStack

app = cdk.App()

msg_stack = MessagingStack(app, "MessagingStack")
persistence_stack = PersistenceStack(app, "PersistenceStack")
ComputeStack(
    app,
    "ComputeStack",
    # example: let the Lambda use the SQS queue URL as env
    environment={"TRIGGER_QUEUE_URL": msg_stack.trigger_queue.queue_url},
)

app.synth()