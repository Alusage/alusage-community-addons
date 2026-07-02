/**
 * Service pour communiquer avec Odoo via JSON-RPC
 * Compatible Odoo 18.0
 */
export class OdooService {
  constructor() {
    this.sessionInfo = window.odooSessionInfo || {};
  }

  /**
   * Appel JSON-RPC générique vers Odoo
   */
  async call(model, method, args = [], kwargs = {}) {
    try {
      const response = await fetch('/web/dataset/call_kw', {
        method: 'POST',
        credentials: 'same-origin', // Important pour envoyer le cookie de session
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          jsonrpc: '2.0',
          method: 'call',
          params: {
            model,
            method,
            args,
            kwargs
          },
          id: Math.floor(Math.random() * 1000000)
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Gestion des erreurs Odoo
      if (data.error) {
        // Code 100 = session expirée
        if (data.error.code === 100) {
          console.warn('Session expirée, redirection vers login');
          window.location.href = '/web/login';
          return;
        }
        throw new Error(data.error.message || 'Erreur Odoo');
      }

      return data.result;
    } catch (error) {
      console.error('Erreur appel Odoo:', error);
      throw error;
    }
  }

  /**
   * Recherche et lecture d'enregistrements
   */
  async searchRead(model, domain = [], fields = []) {
    return this.call(model, 'search_read', [], { domain, fields });
  }

  /**
   * Lecture d'enregistrements par IDs
   */
  async read(model, ids, fields = []) {
    return this.call(model, 'read', [ids], { fields });
  }

  /**
   * Récupérer les informations de l'utilisateur connecté
   */
  async getCurrentUser() {
    try {
      // D'abord essayer avec les infos de session
      if (this.sessionInfo.uid) {
        const users = await this.read('res.users', [this.sessionInfo.uid], [
          'name', 'email', 'login', 'partner_id'
        ]);
        return users[0];
      }

      // Sinon, appeler l'endpoint direct
      const response = await fetch('/my-pwa-app/user-info', {
        credentials: 'same-origin'
      });

      if (!response.ok) {
        throw new Error('Impossible de récupérer les infos utilisateur');
      }

      return await response.json();
    } catch (error) {
      console.error('Erreur récupération utilisateur:', error);
      throw error;
    }
  }

  /**
   * Test de connexion simple
   */
  async testConnection() {
    try {
      const result = await this.call('res.users', 'read', [[this.sessionInfo.uid]], {
        fields: ['name']
      });
      return { success: true, data: result };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }
}