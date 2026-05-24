#!/bin/bash
# init_sandbox.sh - Initialise l'environnement de l'agent

echo "🔧 Initialisation de la Sandbox AgentForge..."

# 1. Configuration de GitHub CLI (gh)
if [ -n "$GITHUB_TOKEN" ]; then
    echo "🔑 Configuration de GitHub CLI..."
    echo "$GITHUB_TOKEN" | gh auth login --with-token
    gh auth setup-git
    git config --global user.email "agent@agentforge.ai"
    git config --global user.name "AgentForge AI"
    echo "✅ GitHub CLI configuré."
else
    echo "⚠️ GITHUB_TOKEN manquant, GitHub CLI ne sera pas authentifié."
fi

# 2. Vérification des dépendances Slack
if [ -n "$SLACK_BOT_TOKEN" ]; then
    echo "✅ Configuration Slack détectée."
else
    echo "⚠️ SLACK_BOT_TOKEN manquant."
fi

# 3. Installation des dépendances du projet (si pyproject.toml ou requirements.txt existe)
if [ -f "requirements.txt" ]; then
    echo "📦 Installation des dépendances Python..."
    pip install -r requirements.txt
fi

echo "🚀 Sandbox prête pour l'exécution."
exec "$@"
