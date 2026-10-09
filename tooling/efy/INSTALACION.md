# Habilidades y herramientas EFY

Paquete aportado por la usuaria el 9 de octubre de 2026. Se verificaron los 898
archivos del manifiesto SHA256 antes de instalar. El ZIP original y su guía de marca
se conservan aquí para reproducir la instalación; son referencias y no solicitudes
para ejecutar todos los procedimientos o conectar los servicios que mencionan.

Instaladas 35 habilidades únicas, con una copia para Codex en `.agents/skills/` y
otra para Claude en `.claude/skills/`. Solo se eligió una variante de frontend-design.
Las referencias cloud, incluida la comparación de seguros incompleta, se conservan
en el paquete y no se presentan como habilidades completas nuevas.

Para instalar o refrescar en este entorno, con Python 3 y Node >=22.12:

```sh
cd /workspace/Webefy
python3 tooling/efy/install.py
```

El instalador preserva archivos existentes y se detiene si difieren del paquete.
Las habilidades ya idénticas no se copian de nuevo. Los runtimes se instalan con
sus locks en `/workspace/tools/EFY-SKILLS-COMPLETAS-2026-10-09/runtimes/`, separados
por completo de `public/` y de las dependencias de la web.

Herramientas incluidas y comprobadas:

- HyperFrames 0.8.113: CLI y diagnóstico; Chromium del entorno como navegador.
- FFmpeg y FFprobe 7.0.2: generación y lectura de un vídeo de un segundo verificadas.
- Playwright CLI 0.1.22: instalación y CLI; página probada con el navegador del entorno.
- AnimateIcons 0.6.0 con React 18.3.1: icono BellIcon renderizado como SVG.

Para HyperFrames:

```sh
HYPERFRAMES_BROWSER_PATH=/usr/bin/chromium node /workspace/tools/EFY-SKILLS-COMPLETAS-2026-10-09/runtimes/hyperframes/hyperframes.mjs --version
```

El doctor de HyperFrames informa como ausentes los modelos opcionales de voz,
transcripción y música (Whisper, Kokoro y MusicGen). No vienen en el paquete y no
impiden el vídeo básico. Las herramientas privadas de documentos, plugins, MCP,
cuentas y servicios externos necesitan capacidades o conexiones independientes:
copiar sus instrucciones no los instala ni concede acceso.

Para esta página se usaron frontend-design y la guía de marca. El brief de la
usuaria —una página de espera más limpia— prevalece sobre ejemplos oscuros del CRM.
No se ejecutaron procedimientos de ese CRM ni se trasladaron sus credenciales.
