import { createClient } from 'redis';

// Create a Redis client for subscribing
const subscriber = createClient();

subscriber.on('connect', () => {
  console.log('Redis client connected to the server');
});

subscriber.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err.message}`);
});

// Subscribe to the "holberton school channel"
subscriber.subscribe('holberton school channel');

// Handle incoming messages
subscriber.on('message', (channel, message) => {
  console.log(message); // Log the message

  // Unsubscribe and quit if message is "KILL_SERVER"
  if (message === 'KILL_SERVER') {
      subscriber.unsubscribe();
      subscriber.quit();
  }
});

