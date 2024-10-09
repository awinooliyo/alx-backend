// Redis and Promisify Setup
const redis = require('redis');
const { promisify } = require('util');

// Create Redis client
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Function to reserve seats
async function reserveSeat(number) {
  await setAsync('available_seats', number);
}

// Function to get the current number of available seats
async function getCurrentAvailableSeats() {
  const seats = await getAsync('available_seats');
  return seats ? parseInt(seats) : 0;
}

// Initialize available seats to 50 and enable reservations
reserveSeat(50);
let reservationEnabled = true;

// Kue Queue Setup
const kue = require('kue');
const queue = kue.createQueue();

// Express Server Setup
const express = require('express');
const app = express();
const port = 1245;

// Route to get the current number of available seats
app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats });
});

// Route to reserve a seat
app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  // Create and queue a new reservation job
  const job = queue.create('reserve_seat').save((err) => {
    if (!err) {
      return res.json({ status: 'Reservation in process' });
    } else {
      return res.json({ status: 'Reservation failed' });
    }
  });

  // Job completion
  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  // Job failure
  job.on('failed', (errorMessage) => {
    console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
  });
});

// Route to process the queue
app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    let availableSeats = await getCurrentAvailableSeats();
    if (availableSeats <= 0) {
      reservationEnabled = false;
      return done(new Error('Not enough seats available'));
    }

    // Decrease available seats by 1
    await reserveSeat(availableSeats - 1);
    availableSeats = await getCurrentAvailableSeats();

    if (availableSeats === 0) {
      reservationEnabled = false;
    }
    done();
  });
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});

// Error handling for Redis connection
client.on('error', (err) => {
  console.log('Error connecting to Redis:', err);
});
