# Repo Name 

What does your repo do

## Features

* API interface for:
    * Client to get public VAPID
    * Store subscription infromation in Klaviyo
    * Receive push data and send to brwoser subscription service
* Serves client application that communicate with back end and installs service work on browser

## Limitations

* web push will only work for users already identified in klavyio

## Klaviyo Features + Endpoints Used


* `Profile` API
* `Event` API
* Flow Webhooks

## Local Development

* Generate VAPIDs (Voluntary Application Server Identification)
* Copy `example.env` to `.env`
* run `docker-compose -f docker-compose-dev.yml up -d --build`
* Go to `http://localhost:8000/docs` to view the API documentation

## Add the Serive Worker
To be properly registered, the service worker requires to be hosted by the site directly and not the middleware. Copy `/examples/sw.js` to be hosted (same domain as the site) and ensure `SERVICE_WORKER_URL` is updated.

## Usage

Example usage here

## FAQ

Q: Question1?

A: Answer1.
