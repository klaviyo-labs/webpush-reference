'use strict';

self.addEventListener('push', function(event) {
  console.log('[Service Worker] Push Received.');
  console.log(`[Service Worker] Push had this data: "${event.data.text()}"`);

  const title = 'Klaviyo';
  const options = {
    body: `"${event.data.text()}"`,
    icon: './images/logo.png',
    badge: './images/logo.png',
    data: {url: event.currentTarget.registration.scope}
  };

  event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', function(event) {
  console.log('[Service Worker] Notification click Received.');

  event.notification.close();

  event.waitUntil(
    clients.openWindow(event.notification.data.url)
  );
});
