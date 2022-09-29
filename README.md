# Web push Reference

Middleware for hosting your own web push services, backed by Klaviyo CDP.

## Features

* API interface for:
    * Getting the main js for push onsite interactions
    * Store web push subscription information in Klaviyo
    * Receive push data and send to browser subscription service
        * Notifies Klaviyo in the event push fails
* Service worker and `index.html` example to host separately. 

## Limitations

* Web push will only work for users already identified in Klaviyo
* Currently, web push relies on flow webhooks to trigger sends. Campaigns are not available


## Klaviyo Features + Endpoints Used

* `GET Profile` API
* `POST Event` API
* Flow Webhooks

## Testing

* Generate VAPIDs (Voluntary Application Server Identification)
    * There are many online services to generate these VAPID keys, however the easiest locally is with web-push npm package.
    * ```bash
        npm install web-push -g
        web-push generate-vapid-keys
      ```
* Copy `example.env` to `.env`.
    * `KLAVIYO_PRIVATE_KEY` Klaviyo [private key](https://help.klaviyo.com/hc/en-us/articles/115005062267-How-to-Manage-Your-Account-s-API-Keys#generate-a-private-api-key3)
    * `SITE_WORKER_URL` Branded site for push e.g. `https://mysite.com`
    * `SERVER_URL` Push URL e.g. `https://mypushserver.com`
    * `VAPID_PRIVATE_KEY` Private key generated above
    * `VAPID_PUBLIC_KEY` Public key generated above
    * `VAPID_MAIL_TO` branded email e.g. `admin@mysite.com`
* run `docker-compose -f docker-compose-dev.yml up -d --build`
* Go to `SERVER_URL/docs` to view the API documentation
* On your branded site add and edit the files found in `examples` and add them to your hosted site as necessary

## Usage

After a user subscribes to web push, the push token and custom message can be used within the
context for a flow webhook. The JSON body should be the following (update `message` as desired):

```json
{
  "message": "Example Klaviyo Web Push from a Flow Webhook!",
  "b64_push_auth": "{{ person.b64_push_auth|default:'' }}",
  "kl_id": "{{person|lookup:'KlaviyoID'}}"
}
```

## FAQ

Q: Question1?

A: Answer1.
