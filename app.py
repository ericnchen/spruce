# -*- coding: utf-8 -*-
import os

import boto3
from botocore.vendored import requests
from chalice import Chalice, IAMAuthorizer


def get_stage() -> str:
    """Return the Amazon API Gateway stage currently deployed to."""
    return os.environ["STAGE"]


def stage_is_dev() -> bool:
    """Return True if the API Gateway stage currently deployed to is dev."""
    return get_stage() == "dev"


app = Chalice(app_name="spruce")

# Since dev mode has debug turned on, only allow authorized IAM roles.
app.debug = True if stage_is_dev() else False
auth_kwargs = {
    "api_key_required": False if stage_is_dev() else True,
    "authorizer": IAMAuthorizer() if stage_is_dev() else None,
}


@app.route("/notify/slack", methods=["POST"], **auth_kwargs)
def notify_slack() -> None:
    """Post a message to the Slack channel for the current API Gateway stage."""
    url = get_secret(f"slack_url_{get_stage().lower()}")
    requests.post(url, json={"text": get_parameter("message")})


def get_parameter(key: str) -> str:
    """Return the specified parameter from the request body."""
    return app.current_request.json_body["parameters"][key]


def get_secret(key: str) -> str:
    """Return the specified secret stored in AWS System Manager."""
    ssm = boto3.client("ssm")
    return ssm.get_parameter(Name=key, WithDecryption=True)["Parameter"]["Value"]
