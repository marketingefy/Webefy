# Consulta de cobertura de Coopartamos

El acceso está en Inicio y en Asistencias → Cobertura de cooperativas. El generador
`scripts/build_site.py` conserva ambas versiones de `coberturas-cooperativas.html`
(raíz y `/nueva/`). La consulta requiere confirmar la cooperativa, escribir la
cédula propia y autorizar su uso para esta consulta.

## Conexión del servidor

El navegador llama únicamente a `/nueva/api/coberturas.php`. El PHP lee la
configuración privada creada en HostGator:

`/home1/brayanez/efy-secrets/masivos.php`

Ese archivo debe devolver un arreglo con `MASIVOS_API_KEY` y
`EFYANALYZER_URL` (`https://app.latamyanez.com`). La clave no se copia al
repositorio, a los recursos públicos, al chat ni a GitHub Actions. El despliegue
transfiere sólo `public/` y conserva ese archivo privado.

El PHP envía `POST` a
`https://app.latamyanez.com/api/integraciones/masivos/coopartamos/consulta`,
con Bearer y cuerpo JSON `{"cedula":"0000000001"}`. El identificador de este
ejemplo es ficticio. Consulta el
[contrato de EfyAnalyzer](https://github.com/brazio1994/efy-analyzer/blob/main/docs/masivos-api.md)
para mantener la equivalencia de campos. El destino HTTPS es fijo, sin
redirecciones, con verificación TLS, un límite de ocho segundos y respuestas
de hasta 256 KiB.

HostGator necesita PHP con cURL, sesiones y acceso de salida HTTPS al destino.
`GET` devuelve disponibilidad local, versión y token CSRF; no lee la cartera ni
verifica por sí solo la validez remota de la clave. El chequeo de publicación
comprueba esa disponibilidad y hace una consulta con el identificador ficticio
documentado por la API, sin imprimir ni guardar resultados. Así valida la clave
y la conexión de HostGator a EfyAnalyzer sin extraer el secreto.

## Datos y resultados

Se conservan todas las coincidencias, incluidas vigencias futuras o vencidas.
El estado lo determina EfyAnalyzer. La web muestra aseguradora, contrato, inicio,
fin y estado. `fecha_consulta` es una fecha `YYYY-MM-DD`, calculada en Ecuador.
Los datos de nombre, cédula, nacimiento, género y procedencia se descartan en el
PHP y no se devuelven al navegador.

Proassislife tiene la cartera disponible. Privilegio está pendiente de carga;
se mantiene ese aviso visible. Cero coincidencias no confirma ausencia de seguro.
Un fallo, una clave incorrecta, un límite o una respuesta inválida muestran
indisponibilidad y permiten contactar al equipo operativo de Efy.

La API todavía no entrega modalidad, beneficios, logos ni teléfonos del convenio.
No se deducen a partir de otros campos. Se conserva una indicación condicional
para titular más familia: registro de dependientes en la primera llamada.

## Protección y comprobación

Las solicitudes usan JSON, sesión HttpOnly/SameSite, CSRF y validación de origen.
Las respuestas llevan `no-store`. No se guardan cédulas, respuestas ni claves en
logs o almacenamiento del navegador. El directorio privado `.efy-masivos`, junto
a `public_html`, guarda únicamente sal aleatoria y marcas de tiempo por una
huella de IP; limita a diez consultas por visitante cada quince minutos.

Para pruebas locales aisladas se pueden configurar `EFY_MASIVOS_CONFIG_FILE`
y `EFY_MASIVOS_STATE_DIR`, siempre fuera del directorio público. Las pruebas
usan una clave ficticia y un transporte simulado; no consultan afiliaciones
reales. Ejecutar los chequeos descritos en `tests/coverage/` y
`node tests/ui/coverage.spec.cjs` después de regenerar el sitio.

La verificación real se ejecuta después de publicar la integración. La clave
permanece en el servidor durante esa prueba.
