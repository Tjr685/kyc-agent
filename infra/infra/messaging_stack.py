from aws_cdk import (
    Duration, Stack,
    aws_sqs as sqs,
    aws_events as events,
    aws_events_targets as targets,
)
from constructs import Construct

class MessagingStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        self.trigger_queue = sqs.Queue(
            self, "TriggerQueue",
            visibility_timeout=Duration.seconds(60),
            dead_letter_queue=sqs.DeadLetterQueue(
                max_receive_count=5,
                queue=sqs.Queue(self, "TriggerDLQ")
            )
        )

        events.Rule(
            self, "WeeklyRule",
            schedule=events.Schedule.rate(Duration.days(7)),
            targets=[targets.SqsQueue(self.trigger_queue)]
        )
