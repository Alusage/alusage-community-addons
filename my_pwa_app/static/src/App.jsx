import React, { useState, useEffect } from 'react';
import { OdooService } from './services/odoo.js';
import './App.css';

const odooService = new OdooService();

function App() {
  const [userInfo, setUserInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [connectionTest, setConnectionTest] = useState(null);

  useEffect(() => {
    loadUserInfo();
  }, []);

  const loadUserInfo = async () => {
    try {
      setLoading(true);
      setError(null);

      // Test de connexion
      const testResult = await odooService.testConnection();
      setConnectionTest(testResult);

      // Récupération des infos utilisateur
      const user = await odooService.getCurrentUser();
      setUserInfo(user);

    } catch (err) {
      setError(err.message);
      console.error('Erreur chargement utilisateur:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="app-container">
        <div className="loading-card">
          <h1>⚡ Chargement...</h1>
          <p>Récupération de votre profil</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app-container">
        <div className="error-card">
          <h1>❌ Erreur</h1>
          <p>{error}</p>
          <button onClick={loadUserInfo} className="retry-button">
            🔄 Réessayer
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="app-container">
      <div className="main-card">
        <header className="card-header">
          <h1>🏰 Portail PWA - Phase 0</h1>
          <p>Test d'authentification et connexion Odoo 18.0</p>
        </header>

        <div className="content-grid">
          {/* Informations utilisateur */}
          <div className="info-section">
            <h2>👤 Utilisateur Connecté</h2>
            <div className="info-grid">
              <div className="info-item">
                <label>ID :</label>
                <span className="value">{userInfo?.id}</span>
              </div>
              <div className="info-item">
                <label>Nom :</label>
                <span className="value">{userInfo?.name}</span>
              </div>
              <div className="info-item">
                <label>Email :</label>
                <span className="value">{userInfo?.email || 'Non défini'}</span>
              </div>
              <div className="info-item">
                <label>Login :</label>
                <span className="value">{userInfo?.login}</span>
              </div>
              <div className="info-item">
                <label>Partenaire ID :</label>
                <span className="value">{userInfo?.partner_id}</span>
              </div>
            </div>
          </div>

          {/* Statut des permissions */}
          <div className="status-section">
            <h2>🔐 Permissions</h2>
            <div className="status-grid">
              <div className={`status-item ${userInfo?.is_portal ? 'active' : 'inactive'}`}>
                <span className="status-icon">{userInfo?.is_portal ? '✅' : '❌'}</span>
                <span>Utilisateur Portal</span>
              </div>
              <div className={`status-item ${userInfo?.is_internal ? 'active' : 'inactive'}`}>
                <span className="status-icon">{userInfo?.is_internal ? '✅' : '❌'}</span>
                <span>Utilisateur Interne</span>
              </div>
            </div>
          </div>

          {/* Test de connexion JSON-RPC */}
          <div className="test-section">
            <h2>🔗 Test JSON-RPC</h2>
            <div className={`connection-status ${connectionTest?.success ? 'success' : 'error'}`}>
              <span className="status-icon">
                {connectionTest?.success ? '✅' : '❌'}
              </span>
              <div>
                <strong>
                  {connectionTest?.success ? 'Connexion réussie' : 'Échec de connexion'}
                </strong>
                {connectionTest?.error && (
                  <p className="error-details">{connectionTest.error}</p>
                )}
              </div>
            </div>
            <button onClick={loadUserInfo} className="test-button">
              🔄 Relancer le test
            </button>
          </div>

          {/* Informations session */}
          <div className="session-section">
            <h2>📋 Session Info</h2>
            <div className="session-details">
              <pre>{JSON.stringify(window.odooSessionInfo || {}, null, 2)}</pre>
            </div>
          </div>
        </div>

        <footer className="card-footer">
          <p>✅ Phase 0 - MVP Minimum Viable Product</p>
          <p>🎯 Objectif : Valider l'intégration Odoo 18.0 ↔ React</p>
        </footer>
      </div>
    </div>
  );
}

export default App;