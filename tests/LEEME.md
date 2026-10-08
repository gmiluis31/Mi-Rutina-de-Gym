# Pruebas automáticas
Requisitos: `pip install playwright` y `playwright install chromium`.
Ejecuta cada archivo con `python tests/<archivo>.py` (usa `www/index.html`). Cada uno imprime los resultados y "errores []" si no hubo fallos de JavaScript.
`h.py` abre automáticamente los menús y hojas del diseño (menú ⋮, Rutinas, Añadir ejercicio) cuando una prueba usa sus controles.
- `cuenta_local.py`: registro, inicio/cierre de sesión y borrado de cuenta (modo local).
- `firebase_simulado.py`: Firebase falso (sin internet): registro, errores de acceso, sincronización por partes, fusión de cambios entre dos dispositivos sin conexión, 3 años de historial, migración del formato antiguo y borrado de cuenta.
- `rutina_por_semana.py`: cada semana con su propia rutina, herencia hacia delante, restablecer y plantillas.
- `biblioteca_y_modo.py`: biblioteca de ejercicios, enlace por alias, modo entrenamiento y resumen.
- `reiniciar_dia.py`, `temporizador.py`, `copiar_reordenar_notas.py`, `mejoras_v2.py`, `tamanos_tactiles.py`.
- `robustez.py`: botón atrás de Android, cambio de día pasada la medianoche, doble toque accidental y foco en Perfil.
- `casos_limite.py`: fechas en 6 husos horarios (cambios de hora, bisiestos, fin de año), texto malicioso, edición de series y arranque con datos guardados corruptos.
- `usuario_caotico.py <semilla> <pasos> <ancho>`: pulsa y escribe al azar vigilando errores de JavaScript, textos "NaN/undefined" y desbordes (por ejemplo `python tests/usuario_caotico.py 1 150 390`).
