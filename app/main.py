from email import message
import os
from typing import Union

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pywebpush import webpush, WebPushException
from klaviyo_sdk import Client

VAPID_CLAIMS = {"sub": "mailto:admin@klaviyo.com"}

app = FastAPI()

client = Client(os.environ.get("KLAVIYO_PRIVATE_KEY"), max_delay=60, max_retries=3)


class PushMessage(BaseModel):
    message: str = "This is a test message!"
    subscription_information: dict


def send_web_push(subscription_information, message_body):
    return webpush(
        subscription_info=subscription_information,
        data=message_body,
        vapid_private_key=os.environ.get("VAPID_PRIVATE_KEY"),
        vapid_claims=VAPID_CLAIMS,
    )


def send_klaviyo_track(subscription_information):
    data = {
        "token": os.environ.get("KLAVIYO_PUBLIC_KEY"),
        "event": "Subscribed to Web Push",
        "customer_properties": {
            "$email": "test.user@klaviyo.com"
        },  # TODO make dyanmic from client code
        "properties": subscription_information,
    }
    client.TrackIdentify.track_post(data=data)


@app.get("/public_key")
async def get_public_key():
    return {"public_key": os.environ.get("VAPID_PUBLIC_KEY")}


@app.post("/subscription", status_code=201)
async def store_subscription(subscription_information: dict):
    send_klaviyo_track(subscription_information=subscription_information)
    return {"Success": 1}


@app.post("/push")
async def push(push_message: PushMessage):
    try:
        send_web_push(push_message.subscription_information, push_message.message)
        return {"Success": 1}
    except WebPushException as e:
        return {"Failed": str(e)}
