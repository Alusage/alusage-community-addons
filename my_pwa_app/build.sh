#!/bin/bash

# Script de build pour le module PWA Odoo
# Phase 0 - MVP

echo "🏗️  Building PWA Module - Phase 0"
echo "=================================="

# Se déplacer dans le répertoire static
cd static

# Vérifier que npm est installé
if ! command -v npm &> /dev/null; then
    echo "❌ npm n'est pas installé"
    exit 1
fi

# Installer les dépendances si node_modules n'existe pas
if [ ! -d "node_modules" ]; then
    echo "📦 Installation des dépendances npm..."
    npm install
fi

# Build de l'application React
echo "⚛️  Compilation de l'application React..."
npm run build

# Vérifier que le build s'est bien passé
if [ -f "dist/index.js" ] && [ -f "dist/index.css" ]; then
    echo "✅ Build réussi !"
    echo "📁 Fichiers générés :"
    ls -la dist/
    echo ""
    echo "🚀 Pour tester :"
    echo "   1. Installer le module dans Odoo"
    echo "   2. Aller sur /my-pwa-app"
    echo "   3. Vérifier l'authentification"
else
    echo "❌ Échec du build"
    exit 1
fi