'use strict';

self.addEventListener('push', function(event) {
  console.log('[Service Worker] Push Received.');
  console.log(`[Service Worker] Push had this data: "${event.data.text()}"`);

  const title = 'Michael Worthley';
  const options = {
    body: `"${event.data.text()}"`,
    icon: 'https://www.klaviyo.com/wp-content/uploads/2022/03/favicon.png',
    badge: 'https://www.klaviyo.com/wp-content/uploads/2022/03/favicon.png'
  };

  event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', function(event) {
  console.log('[Service Worker] Notification click Received.');

  event.notification.close();

  event.waitUntil(
    clients.openWindow('https://')
  );
});