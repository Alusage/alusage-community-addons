#!/bin/bash

# Script de vérification pour Phase 0
# Vérifie que tous les fichiers nécessaires sont présents

echo "🔍 Vérification Phase 0 - MVP"
echo "=============================="

ERROR_COUNT=0

# Fonction pour vérifier un fichier
check_file() {
    if [ -f "$1" ]; then
        echo "✅ $1"
    else
        echo "❌ $1 manquant"
        ((ERROR_COUNT++))
    fi
}

# Fonction pour vérifier un répertoire
check_dir() {
    if [ -d "$1" ]; then
        echo "✅ $1/"
    else
        echo "❌ $1/ manquant"
        ((ERROR_COUNT++))
    fi
}

echo ""
echo "📁 Structure du module :"
check_file "__manifest__.py"
check_file "__init__.py"
check_file "README.md"
check_file "build.sh"

echo ""
echo "🎮 Controllers :"
check_dir "controllers"
check_file "controllers/__init__.py"
check_file "controllers/main.py"

echo ""
echo "🗃️ Models :"
check_dir "models"
check_file "models/__init__.py"

echo ""
echo "🔐 Security :"
check_dir "security"
check_file "security/ir.model.access.csv"

echo ""
echo "🌐 Views :"
check_dir "views"
check_file "views/templates.xml"

echo ""
echo "⚛️ Frontend React :"
check_dir "static"
check_file "static/package.json"
check_file "static/vite.config.js"
check_file "static/index.html"

echo ""
echo "📦 Source React :"
check_dir "static/src"
check_file "static/src/main.jsx"
check_file "static/src/App.jsx"
check_file "static/src/App.css"

echo ""
echo "🔗 Services :"
check_dir "static/src/services"
check_file "static/src/services/odoo.js"

echo ""
echo "🏗️ Build :"
check_dir "static/dist"
check_file "static/dist/index.js"
check_file "static/dist/index.css"

echo ""
echo "=============================="

if [ $ERROR_COUNT -eq 0 ]; then
    echo "✅ Tous les fichiers sont présents !"
    echo ""
    echo "🚀 Phase 0 prête pour test :"
    echo "   1. Copier le module dans Odoo addons/"
    echo "   2. Installer le module via l'interface"
    echo "   3. Naviguer vers /my-pwa-app"
    echo "   4. Vérifier l'affichage des infos utilisateur"
    echo ""
    echo "📋 Fonctionnalités à tester :"
    echo "   • Authentification automatique"
    echo "   • Affichage ID, nom, email utilisateur"
    echo "   • Test connexion JSON-RPC"
    echo "   • Interface responsive"
    exit 0
else
    echo "❌ $ERROR_COUNT fichier(s) manquant(s)"
    echo ""
    echo "🔧 Pour corriger :"
    echo "   ./build.sh  # Rebuild si nécessaire"
    exit 1
fi