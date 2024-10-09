// Product Data
const listProducts = [
  { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 },
];

// Function to get a product by id
function getItemById(id) {
  return listProducts.find(product => product.itemId === id);
}

// Redis Integration
const redis = require('redis');
const { promisify } = require('util');

// Create Redis client
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Function to reserve stock by itemId in Redis
function reserveStockById(itemId, stock) {
  return setAsync(`item.${itemId}`, stock);
}

// Function to get the reserved stock by itemId from Redis
async function getCurrentReservedStockById(itemId) {
  const stock = await getAsync(`item.${itemId}`);
  return stock ? parseInt(stock) : null;
}

// Express Server
const express = require('express');
const app = express();
const port = 1245;

// Route to list all products
app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

// Route to get product details and current stock by itemId
app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const product = getItemById(itemId);

  if (!product) {
    return res.json({ status: 'Product not found' });
  }

  const currentStock = await getCurrentReservedStockById(itemId) || product.initialAvailableQuantity;
  res.json({ ...product, currentQuantity: currentStock });
});

// Route to reserve a product by itemId
app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const product = getItemById(itemId);

  if (!product) {
    return res.json({ status: 'Product not found' });
  }

  const currentStock = await getCurrentReservedStockById(itemId) || product.initialAvailableQuantity;

  if (currentStock <= 0) {
    return res.json({ status: 'Not enough stock available', itemId });
  }

  // Reserve one item and return confirmation
  await reserveStockById(itemId, currentStock - 1);
  return res.json({ status: 'Reservation confirmed', itemId });
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
