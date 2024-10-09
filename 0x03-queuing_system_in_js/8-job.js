export default function createPushNotificationsJobs(jobs, queue) {
  if (!Array.isArray(jobs)) {
    throw new Error('Jobs is not an array');
  }

  jobs.forEach((jobData) => {
    const job = queue.create('push_notification_code_3', jobData).save((err) => {
      if (!err) {
        console.log('Notification job created');
      }
    });

    // Skip event listeners in test mode
    if (queue.testMode) return;

    job.on('complete', () => {
      console.log('Notification job completed');
    });

    job.on('failed', (err) => {
      console.log(`Notification job failed: ${err}`);
    });

    job.on('progress', (progress) => {
      console.log(`Notification job ${progress}% complete`);
    });
  });
}
