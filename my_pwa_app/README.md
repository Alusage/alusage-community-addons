# My PWA App - Phase 0 (MVP)

🎯 **Objectif** : Valider l'intégration Odoo 18.0 ↔ React et l'authentification portal

## 📋 Statut Phase 0

✅ **Implémenté** :
- [x] Structure minimale du module Odoo
- [x] Controller principal avec authentification portal
- [x] Application React basique avec Vite
- [x] Service JSON-RPC pour communication Odoo
- [x] Interface de test affichant les informations utilisateur
- [x] Build automatisé

## 🚀 Installation et Test

### 1. Prérequis
- Odoo 18.0
- Node.js et npm
- Utilisateur avec droits portal ou internes

### 2. Installation
```bash
# 1. Copier le module dans addons/
cp -r my_pwa_app /path/to/odoo/addons/

# 2. Build de l'application React
cd my_pwa_app
./build.sh

# 3. Installer le module dans Odoo
# Via l'interface : Apps > My PWA App > Install
```

### 3. Test
1. **Se connecter à Odoo** avec un utilisateur portal/interne
2. **Naviguer vers** `/my-pwa-app`
3. **Vérifier l'affichage** :
   - ID utilisateur connecté
   - Nom complet
   - Email
   - Status de connexion JSON-RPC

## 🏗️ Structure

```
my_pwa_app/
├── __manifest__.py              # Configuration module Odoo
├── __init__.py
├── build.sh                     # Script de build
├── controllers/
│   ├── __init__.py
│   └── main.py                  # Controller principal (/my-pwa-app)
├── models/
│   └── __init__.py              # Vide pour Phase 0
├── security/
│   └── ir.model.access.csv      # Droits basiques
├── static/
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   ├── src/
│   │   ├── main.jsx             # Point d'entrée React
│   │   ├── App.jsx              # Application principale
│   │   ├── App.css              # Styles
│   │   └── services/
│   │       └── odoo.js          # Service JSON-RPC
│   └── dist/                    # Build généré
│       ├── index.js
│       └── index.css
└── views/
    └── templates.xml            # Template HTML Odoo
```

## 🔧 Fonctionnalités Phase 0

### Controller Odoo (`/my-pwa-app`)
- ✅ Authentification automatique (auth='user')
- ✅ Redirection login si non connecté
- ✅ Vérification droits portal
- ✅ Injection session info dans React
- ✅ Endpoint API test (`/my-pwa-app/user-info`)

### Application React
- ✅ Interface de test avec thème MTG simplifié
- ✅ Affichage informations utilisateur (ID, nom, email, login)
- ✅ Test de connexion JSON-RPC en temps réel
- ✅ Gestion d'erreurs et états de chargement
- ✅ Design responsive

### Service JSON-RPC
- ✅ Communication `/web/dataset/call_kw` (Odoo 18.0)
- ✅ Gestion session cookies automatique
- ✅ Gestion erreurs (session expirée, etc.)
- ✅ Méthodes helpers (read, search_read)

## 🎨 Design

**Phase 0** utilise un design MTG simplifié :
- Fond dégradé slate (noir/gris foncé)
- Bordures dorées
- Typography : Cinzel (titres) + Spectral (corps)
- Couleurs : Gold, Success (vert), Error (rouge)

## 🧪 Tests de Validation

### ✅ Tests Réussis
1. **Authentification** : Redirection automatique vers login si non connecté
2. **JSON-RPC** : Appels réussis vers `/web/dataset/call_kw`
3. **Session** : Cookie de session automatiquement envoyé
4. **Permissions** : Vérification droits portal/internes
5. **Build** : Compilation Vite réussie

### 🔍 À Tester
- [ ] Comportement sur session expirée
- [ ] Performance sur mobile
- [ ] Compatibilité navigateurs

## 📈 Prochaines Étapes

**Phase 1** : Extensions backend Odoo
- Extension `res.users` (XP, level)
- Extension `hr.employee` (stats RPG)
- Extension `gamification.badge` (rareté)
- Modèle `quest` personnalisé

**Phase 2** : Frontend React avancé
- TypeScript complet
- Material UI + thème MTG
- TanStack Query pour cache
- PWA complète

## 🐛 Résolution de Problèmes

### Erreur "Module non trouvé"
```bash
# Vérifier la structure
ls -la my_pwa_app/
# Rebuild
cd my_pwa_app && ./build.sh
```

### Erreur 404 sur /my-pwa-app
- Vérifier que le module est installé
- Redémarrer Odoo après installation
- Vérifier les logs Odoo

### Interface ne charge pas
- Vérifier `dist/index.js` et `dist/index.css` existent
- Ouvrir DevTools > Console pour erreurs JS
- Vérifier session utilisateur connecté

## 📞 Support

Pour toute question Phase 0 : Nicolas JEUDY

---

**Version** : Phase 0 (MVP)
**Dernière mise à jour** : 2025-01-03
**Status** : ✅ Fonctionnel - Prêt pour validation