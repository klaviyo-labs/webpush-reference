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

* `track` API
* Flow Webhooks

## Installation

* Generate VAPIDs (Voluntary Application Server Identification)
* Copy `example.env` to `.env`
* run `docker-compose up -d`

You can go to `http://localhost:8000/docs` to view the API documentation.

## Usage

Example usage here

## FAQ

Q: Question1?

A: Answer1.
