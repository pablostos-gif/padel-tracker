# 📦 Instrucciones de Deploy a Netlify

## ✅ Opción 1: DRAG-DROP Directo (RECOMENDADO - Más rápido)

1. Ve a: https://app.netlify.com/drop
2. Arrastra y suelta el archivo `padel-tracker.html`
3. ¡Listo! Tu sitio estará en vivo en 5 segundos

**Ventaja:** Sin necesidad de credenciales ni configuración

---

## 🔧 Opción 2: Actualizar sitio existente (padel-pablo.netlify.app)

1. Inicia sesión en: https://app.netlify.com
2. Selecciona tu sitio "padel-pablo"
3. Ve a "Deploys"
4. Arrastra y suelta `padel-tracker.html`

---

## 🐙 Opción 3: Conectar con GitHub (Automático)

Si prefieres que los cambios se desplieguen automáticamente:

1. Crea un repositorio en GitHub:
   ```
   Nombre: padel-lucas-app
   URL: https://github.com/pablostos/padel-lucas-app
   ```

2. En tu máquina local, configura:
   ```bash
   git remote set-url origin https://github.com/pablostos/padel-lucas-app.git
   git push -u origin master
   ```

3. En Netlify, conecta tu repositorio:
   - Settings → Linked site → Connect repository
   - Selecciona padel-lucas-app
   - ¡Hecho! Cada push a GitHub = deploy automático

---

## 📝 Cambios en esta versión

- ✅ Fixed: Simulador 3D espera a que THREE.js cargue desde CDN
- ✅ Fixed: Validación de dimensiones del canvas (mín. 100x100px)
- ✅ Improved: Mejor manejo de errores con retry automático

---

## 🧪 Test Local

```bash
# Servidor local ya está corriendo en:
http://localhost:8000/padel-tracker.html

# Prueba:
# 1. Haz clic en "Simulador 3D"
# 2. Debería cargar sin errores
# 3. Controles: WASD para mover, ESPACIO para disparar
```
