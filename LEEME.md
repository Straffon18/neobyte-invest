# NEOBYTE Invest: página que se actualiza sola

## Qué hace cada archivo

| Archivo | Para qué sirve |
|---|---|
| `index.html` | La página |
| `data.json` | Los datos: precios, objetivos y tipo de cambio. El robot lo reescribe solo |
| `scripts/update.py` | El robot que descarga los datos de Yahoo Finanzas |
| `.github/workflows/actualizar.yml` | El horario del robot: cada 30 min de lunes a viernes de 7:30 a 15:00 (hora CDMX), y una vez cada noche |

---

## Opción A (recomendada): todo en GitHub, gratis

1. **Crea el repositorio.** En GitHub, haz uno nuevo y público, por ejemplo `neobyte-invest`.
2. **Sube los archivos.** Pon todo el contenido de esta carpeta, incluida la carpeta oculta `.github`. Si la subes desde la web arrastrando, verifica que `.github/workflows/actualizar.yml` sí se haya subido.
3. **Da permiso al robot.** Ve a **Settings → Actions → General → Workflow permissions** y elige **Read and write permissions**. Guarda.
4. **Prueba el robot.** Entra a la pestaña **Actions → Actualizar datos de bolsa → Run workflow**. En 2–4 minutos debe terminar en verde ✅ y `data.json` tendrá más de 70 empresas.
5. **Publica la página.** Ve a **Settings → Pages**, en *Source* elige **Deploy from a branch**, luego `main` y `/ (root)`.
6. **Conecta tu subdominio.**
   - En **Settings → Pages → Custom domain** escribe `invest.tudominio.com` y guarda.
   - En el panel DNS de tu dominio crea un registro **CNAME**: nombre `invest`, valor `TU-USUARIO.github.io`.
   - Espera de 10 min a unas horas y activa **Enforce HTTPS**.

Listo. No tienes que hacer nada más: el robot actualiza `data.json` y la página toma los datos nuevos sola cada 5 minutos.

## Opción B: la página en tu propio hosting (cPanel, Hostinger, etc.)

1. Haz los pasos 1 a 4 de la Opción A para que el robot corra en GitHub.
2. Abre `index.html` y cambia esta línea:
   ```js
   const DATA_URL='data.json';
   ```
   por:
   ```js
   const DATA_URL='https://raw.githubusercontent.com/TU-USUARIO/neobyte-invest/main/data.json';
   ```
3. Sube **solo** `index.html` a la carpeta de tu subdominio.

---

## Preguntas rápidas

**¿Quiero agregar o quitar empresas?**
Edita la lista `UNIVERSE` en `scripts/update.py`. Usa el ticker de Yahoo: las mexicanas llevan `.MX`, por ejemplo `WALMEX.MX`.

**¿Cada cuándo se actualiza?**
Lo marca el archivo `actualizar.yml`. GitHub a veces retrasa unos minutos las tareas programadas, es normal.

**¿El robot falló?**
Revisa la pestaña Actions. Si Yahoo no responde, el robot conserva el último dato bueno; la página nunca se queda vacía.

**¿De dónde salen los datos?**
De Yahoo Finanzas, con unos 15 minutos de retraso. Los precios objetivo son el promedio de los analistas que siguen a cada empresa. Si una empresa tiene pocos analistas, aparece como "Sin consenso".
