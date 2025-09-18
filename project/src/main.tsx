import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.tsx';
import './index.css';
import { initializeStorage } from './utils/storage';

// Initialize storage (backend or localStorage)
initializeStorage().catch(error => {
  console.error('Failed to initialize storage:', error);
});

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>
);