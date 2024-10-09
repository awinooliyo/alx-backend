import { createClient } from 'redis';
import { promisify } from 'util';

// Create the Redis client
const client = createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err.message}`);
});

// Promisify the 'get' function
const getAsync = promisify(client.get).bind(client);

// Modify displaySchoolValue function to use async/await
async function displaySchoolValue(schoolName) {
  try {
      const value = await getAsync(schoolName);
      console.log(value); // Log the value of the key
  } catch (err) {
      console.error(`Error: ${err}`);
  }
}

// Function to set the new school name and value using callback
function setNewSchool(schoolName, value) {
  client.set(schoolName, value, (err, res) => {
    if (err) {
	  console.error(err);
	} else {
	  console.log(res);
	}
  });
}

// Call the functions
displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
