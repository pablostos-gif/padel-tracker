// Script para extraer datos guardados locales
const fs = require('fs');

// Leer el archivo HTML
const html = fs.readFileSync('padel-tracker.html', 'utf8');

// Buscar datos embebidos en el HTML
const match = html.match(/<script type="application\/json" id="__ptd">([^<]*)<\/script>/);
if (match && match[1] && match[1] !== 'null') {
  try {
    const data = JSON.parse(match[1]);
    console.log('📦 DATOS ENCONTRADOS EN HTML:');
    console.log('Jugador:', data.playerName || '(sin nombre)');
    console.log('Partidos guardados:', data.history ? data.history.length : 0);
    console.log('Entrenamientos guardados:', data.trainings ? data.trainings.length : 0);
    console.log('\n✅ Los datos existen y serán rescatados automáticamente');
    fs.writeFileSync('data-backup.json', JSON.stringify(data, null, 2));
    console.log('💾 Backup guardado en data-backup.json');
  } catch(e) {
    console.log('Error parsing:', e);
  }
} else {
  console.log('⚠️ No se encontraron datos guardados en el HTML');
  console.log('Esto es normal en una primera instalación');
}
