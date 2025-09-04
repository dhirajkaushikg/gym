const express = require('express');
const path = require('path');
const { createServer } = require('node:http');
const { fileURLToPath } = require('node:url');

// Create __dirname equivalent for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

// Set proper MIME types for static files
app.use((req, res, next) => {
  // Set MIME type for JavaScript files
  if (req.url.endsWith('.js')) {
    res.setHeader('Content-Type', 'text/javascript');
  }
  // Set MIME type for WASM files
  else if (req.url.endsWith('.wasm')) {
    res.setHeader('Content-Type', 'application/wasm');
  }
  next();
});

// Serve static files from the dist directory
app.use(express.static(path.join(__dirname, 'dist'), {
  setHeaders: (res, filePath) => {
    // Ensure JavaScript files are served with correct MIME type
    if (filePath.endsWith('.js')) {
      res.setHeader('Content-Type', 'text/javascript');
    }
    // Ensure CSS files are served with correct MIME type
    else if (filePath.endsWith('.css')) {
      res.setHeader('Content-Type', 'text/css');
    }
  }
}));

// Serve the main index.html file for all routes (for client-side routing)
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Something went wrong!');
});

const server = createServer(app);

server.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
  console.log(`Visit http://localhost:${PORT} to view your application`);
});