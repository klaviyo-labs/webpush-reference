from base64 import b64decode, b64encode
import json
import os

from fastapi import BackgroundTasks, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from klaviyo_sdk_beta import Client  # revision "2022-09-07.pre"
from pydantic import BaseModel
from pywebpush import webpush, WebPushException

app = FastAPI()

origins = [os.environ.get("SITE_WORKER_URL")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["POST"],
)

templates = Jinja2Templates(directory="./app/templates")

client = Client(os.environ.get("KLAVIYO_PRIVATE_KEY"), max_delay=60, max_retries=3)


class PushMessage(BaseModel):
    message: str = "Placeholder message"
    b64_push_auth: str
    kl_id: str


class Subscription(BaseModel):
    subscription_information: dict
    kl_exchange: str


def send_web_push(subscription_information, message_body):
    return webpush(
        subscription_info=subscription_information,
        data=message_body,
        vapid_private_key=os.environ.get("VAPID_PRIVATE_KEY"),
        vapid_claims={"sub": os.environ.get("VAPID_MAIL_TO")},
    )


def store_subscription(kl_exchange: str, subscription_information: dict):
    profile = client.Profiles.get_profiles(
        # TODO: API supports it, SDK does not.
        # fields_profile=["id"],
        filter=f'equals(_kx,"{kl_exchange}")',
    )["data"][0]

    b64_push_auth = b64encode(json.dumps(subscription_information).encode()).decode()

    payload = {
        "data": {
            "type": "event",
            "attributes": {
                "profile": {
                    "$kid": profile["id"],
                    "b64_push_auth": b64_push_auth,
                },
                "metric": {"name": "Subscribed to Web Push", "service": "api"},
                "properties": {"b64_push_auth": b64_push_auth},
            },
        }
    }
    client.Events.create_event(
        payload, _preload_content=False
    )  # see: https://github.com/klaviyo/klaviyo-python-sdk-beta/issues/1

    send_web_push(subscription_information, "Push enabled")


def push_subscription(push_message):
    subscription_information = json.loads(b64decode(push_message.b64_push_auth))
    try:
        send_web_push(subscription_information, push_message.message)
        payload = {
            "data": {
                "type": "event",
                "attributes": {
                    "profile": {"$kid": push_message.kl_id},
                    "metric": {"name": "Web Pushed Sent", "service": "api"},
                    "properties": dict(push_message),
                },
            }
        }
        client.Events.create_event(payload, _preload_content=False)
    except WebPushException as push_exception:
        payload = {
            "data": {
                "type": "event",
                "attributes": {
                    "profile": {
                        "$kid": push_message.kl_id,
                        "$unset": ["b64_push_auth"],
                    },
                    "metric": {"name": "Web Pushed Rejected", "service": "api"},
                    "properties": {"reason": str(push_exception)},
                },
            }
        }
        client.Events.create_event(payload, _preload_content=False)


@app.post("/subscription", status_code=201)
async def subscribe_user(subscription: Subscription, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        store_subscription,
        kl_exchange=subscription.kl_exchange,
        subscription_information=subscription.subscription_information,
    )
    return {"Success": 1}


@app.post("/push")
async def push(push_message: PushMessage, background_tasks: BackgroundTasks):
    background_tasks.add_task(push_subscription, push_message=push_message)
    return {"Success": 1}


@app.get("/main.js")
async def get_main_js(request: Request):
    return templates.TemplateResponse(
        "main.js",
        {
            "request": request,
            "server_public_key": os.environ.get("VAPID_PUBLIC_KEY"),
            "server_url": os.environ.get("SERVER_URL"),
            "site_worker_url": os.environ.get("SITE_WORKER_URL"),
        },
    )
