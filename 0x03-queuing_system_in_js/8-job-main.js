import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';

// Create a Kue queue
const queue = kue.createQueue();

// Example list of jobs
const list = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account'
  }
];

// Call the function to create jobs
createPushNotificationsJobs(list, queue);
