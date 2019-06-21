import boto3
import json
import time

from typing import Optional, Union

from .. import env, stages
from ..context import Context


class AWS:
    """Provides access to AWS."""

    _lambda = boto3.client("lambda")
    _function_prefix = env.lambda_function_prefix

    def invoke(self, fn: str, msg: Union[dict, Context]) -> None:
        """Invoke an AWS Lambda function."""
        if isinstance(msg, Context):
            msg = msg.__dict__
        msg["stage"] = fn
        self._lambda.invoke(
            FunctionName=self._function(fn),
            InvocationType="Event",
            Payload=json.dumps(msg),
        )

    def invoke_notify(self, ctx: Context, notification: str):
        """Invokes the notify function."""
        ctx.notification = notification
        self.invoke(stages.notify, ctx)

    def _function(self, fn: str) -> str:
        """Get a Lambda function name."""
        return self._function_prefix + fn