import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

// StrictMode removed intentionally to prevent double-invocation of
// streaming SSE effects which caused duplicate words in chat.
createRoot(document.getElementById('root')).render(
  <App />
)
