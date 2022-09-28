'use strict';

const pushButton = document.querySelector('.push-btn');
const klExchange = _learnq.push(['_getIdentifiers']).$exchange_id

let isSubscribed = false;
let swRegistration = null;

function updateBtn() {
    if (Notification.permission === 'denied') {
        pushButton.textContent = 'Push Messaging Blocked.';
        pushButton.disabled = true;
        updateSubscriptionStatus(null);
        return;
    }

    if (isSubscribed) {
        pushButton.textContent = 'Push Already Enabled';
    } else {
        pushButton.textContent = 'Enable Push Messaging';
        pushButton.disabled = false;
    }
}

function updateSubscriptionStatus(isSubscribed) {
    const subscriptionDetails = document.querySelector('.subscription-details');

	const subscriptionJson = document.querySelector('.subscription-token');
	subscriptionJson.textContent = localStorage.getItem('subscription_token');

    if (isSubscribed) {
        subscriptionDetails.hidden = false;
    } else {
        subscriptionDetails.hidden = true;
    }
}

function updateSubscriptionServer(subscription) {
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var raw = JSON.stringify({subscription_information: subscription, kl_exchange: klExchange});

    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    };

    fetch("{{server_url}}/subscription", requestOptions)
        .then(response => response.text())
        .then(result => console.info(result))
        .catch(error => console.info('error', error));
}


function subscribeUser() {
    const applicationServerKey = localStorage.getItem('applicationServerPublicKey');
    swRegistration.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: applicationServerKey
        })
        .then(function(subscription) {
            console.info('User is subscribed.');

            updateSubscriptionStatus(subscription);
            localStorage.setItem('subscription_token', JSON.stringify(subscription));

            isSubscribed = true;

            updateSubscriptionServer(subscription)

            updateBtn();
        })
        .catch(function(err) {
            console.info('Failed to subscribe the user: ', err);
            updateBtn();
        });
}

function initializeUI() {
    pushButton.addEventListener('click', function() {
        pushButton.disabled = true;
        subscribeUser();
    });

    // Set the initial subscription value
    swRegistration.pushManager.getSubscription()
        .then(function(subscription) {
            isSubscribed = !(subscription === null);
            updateSubscriptionStatus(isSubscribed);
            updateBtn();
        });
}

if ('serviceWorker' in navigator && 'PushManager' in window) {
    localStorage.setItem('applicationServerPublicKey', "{{server_public_key}}");
    console.info('Service Worker and Push is supported');

	if (klExchange) {
		navigator.serviceWorker.register("{{site_worker_url}}/sw.js")
			.then(function(swReg) {
				swRegistration = swReg;
				initializeUI();
			})
			.catch(function(error) {
				console.error('Service Worker Error', error);
			});
	} else {
		pushButton.textContent = 'User Must be identified by Klaviyo';
	}
} else {
    pushButton.textContent = 'Push Not Supported';
}
