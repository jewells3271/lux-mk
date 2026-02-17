import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

const mountId = 'lux-widget-root';
let rootElement = document.getElementById(mountId);
if (!rootElement) {
  rootElement = document.createElement('div');
  rootElement.id = mountId;
  document.body.appendChild(rootElement);
}

createRoot(rootElement).render(
  <StrictMode>
    <App />
  </StrictMode>,
)