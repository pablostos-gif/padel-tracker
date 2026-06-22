@echo off
cd /d "%~dp0"
echo.
echo =====================================
echo  PADEL TRACKER - DEPLOY AHORA
echo =====================================
echo.
echo 1. Se abrira Netlify Drop en tu navegador
echo 2. Arrastra padel-tracker.html a la ventana
echo 3. ¡Espera 30 segundos y listo!
echo.
pause

start https://app.netlify.com/drop
explorer "%cd%"
