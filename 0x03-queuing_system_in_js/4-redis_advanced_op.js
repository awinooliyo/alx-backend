import { createClient } from 'redis';

// Create the Redis client
const client = createClient();

client.on('connect', () => {
    console.log('Redis client connected to the server');
});

client.on('error', (err) => {
    console.log(`Redis client not connected to the server: ${err.message}`);
});

// Store the hash using hset for each city and use redis.print for confirmation
client.hset('HolbertonSchools', 'Portland', 50, console.log);
client.hset('HolbertonSchools', 'Seattle', 80, console.log);
client.hset('HolbertonSchools', 'New York', 20, console.log);
client.hset('HolbertonSchools', 'Bogota', 20, console.log);
client.hset('HolbertonSchools', 'Cali', 40, console.log);
client.hset('HolbertonSchools', 'Paris', 2, console.log);

// Retrieve and display the stored hash using hgetall
client.hgetall('HolbertonSchools', (err, result) => {
    if (err) {
        console.log(err);
    } else {
        console.log(result);
    }
});
