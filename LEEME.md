# Mi rutina de gym — proyecto para Google Play

La app (www/index.html) está envuelta con Capacitor para generar un paquete Android (.aab).

## Antes de empezar
1. Instala Node.js (LTS) y Android Studio (incluye el SDK y JDK).
2. En `capacitor.config.json` cambia `appId` por uno propio y único (ej. `com.tunombre.rutinagym`). No se puede cambiar después de publicar.

## Generar el proyecto Android
```
npm install @capacitor/core @capacitor/cli @capacitor/android
npm install -D @capacitor/assets
npx cap add android
npx capacitor-assets generate --android
npx cap sync android
npx cap open android
```

## Firmar y exportar el .aab (en Android Studio)
1. Antes, en `android/app/build.gradle` sube `versionCode` en cada versión que subas (empieza en 1) y ajusta `versionName`.
2. Menú **Build > Generate Signed App Bundle / APK > Android App Bundle**.
3. Crea un keystore nuevo (**guárdalo y su contraseña en un lugar seguro**; sin él no podrás actualizar la app).
4. Elige **release** y termina. El archivo queda en `android/app/release/app-release.aab`.
(Si Play App Signing te lo ofrece, acéptalo: es lo recomendado.)

## Subir a Google Play
1. Crea una cuenta en Google Play Console (tiene un pago único de registro).
2. **Crear app** → idioma Español, tipo App, gratuita.
3. Completa en el panel: ficha (store/ficha-play-store.md), política de privacidad (publica store/politica-privacidad.md en una URL pública, por ejemplo GitHub Pages, y pega el enlace), clasificación de contenido, seguridad de los datos, público objetivo y anuncios.
4. Sube el .aab a una pista de prueba (interna/cerrada) o a producción y envía a revisión.
5. Las cuentas personales nuevas suelen requerir una prueba cerrada con testers durante un periodo antes de pasar a producción. Revisa los requisitos vigentes en Play Console, incluido el nivel de API objetivo (targetSdk) mínimo; actualiza Capacitor si lo exige.

## Contenido
- `www/` la app
- `assets/` icono y splash (fuente para `capacitor-assets`)
- `store/` textos, política de privacidad, icono 512 y gráfico de función 1024×500

## APK para instalar en tu móvil (sin Android Studio)
1. Crea un repositorio en GitHub y sube el contenido de esta carpeta (rama `main`).
2. Ve a la pestaña **Actions → Compilar APK → Run workflow** (también corre solo al subir cambios).
3. Cuando termine, abre la ejecución y descarga **mi-rutina-gym-apk** (viene dentro de un zip con `app-debug.apk`).
4. Pasa el APK al móvil, ábrelo y permite "instalar apps de orígenes desconocidos" cuando te lo pida.
Este APK es de prueba (firma de depuración): sirve para instalarlo tú, no para subirlo a Google Play. Para Play usa el .aab firmado de la sección anterior.
