#!/bin/bash

echo "🚀 Desplegando Pádel Tracker..."

# Configurar Git si no está configurado
if ! git config user.email > /dev/null 2>&1; then
  git config user.email "pablo@padel.app"
  git config user.name "Pablo"
fi

# Agregar cambios
git add -A
git commit -m "Update: Pádel Tracker - Latest changes $(date +%Y-%m-%d\ %H:%M:%S)" || echo "No new changes to commit"

# Detectar repositorio remoto
REMOTE=$(git config --get remote.origin.url)

if [ -z "$REMOTE" ]; then
  echo "⚠️  No se encontró repositorio remoto configurado"
  echo ""
  echo "Opción 1: Si tienes repositorio en GitHub:"
  echo "  git remote add origin <tu-url-github>"
  echo "  git push -u origin master"
  echo ""
  echo "Opción 2: Deploy directo a Netlify:"
  echo "  npm install -g @netlify/cli"
  echo "  netlify deploy --dir=. --prod"
  echo ""
  echo "Opción 3: Sube manualmente a:"
  echo "  https://app.netlify.com/drop"
  echo "  (Arrastra y suelta padel-tracker.html)"
else
  echo "📡 Remoto detectado: $REMOTE"
  git push -u origin master
  echo "✅ Deploy completado!"
fi
