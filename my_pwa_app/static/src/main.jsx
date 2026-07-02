import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'

// Vérifier que le DOM est chargé
document.addEventListener('DOMContentLoaded', () => {
  const rootElement = document.getElementById('root');

  if (rootElement) {
    console.log('🚀 Initialisation de l\'application PWA - Phase 0');
    console.log('📋 Session info:', window.odooSessionInfo);

    const root = ReactDOM.createRoot(rootElement);
    root.render(
      <React.StrictMode>
        <App />
      </React.StrictMode>
    );
  } else {
    console.error('❌ Élément root non trouvé');
  }
});

// Fallback si DOMContentLoaded déjà passé
if (document.readyState === 'loading') {
  // Le code ci-dessus s'exécutera
} else {
  // DOM déjà chargé
  const rootElement = document.getElementById('root');

  if (rootElement) {
    console.log('🚀 Initialisation de l\'application PWA - Phase 0 (DOM déjà chargé)');
    console.log('📋 Session info:', window.odooSessionInfo);

    const root = ReactDOM.createRoot(rootElement);
    root.render(
      <React.StrictMode>
        <App />
      </React.StrictMode>
    );
  }
}