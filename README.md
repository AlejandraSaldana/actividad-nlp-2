# Calculadora en Python

Proyecto de clase de [AlejandraSaldana/actividad-nlp-2](https://github.com/AlejandraSaldana/actividad-nlp-2): calculadora con menú interactivo, API y comprobaciones automáticas de funcionamiento, cobertura y seguridad.

## Preparar el entorno

Requiere Python 3.12 o posterior. Desde la carpeta del repositorio:

```text
python -m venv .venv
```

Activa el entorno según tu terminal:

| Terminal | Comando |
| --- | --- |
| Windows, Símbolo del sistema | `.venv\Scripts\activate.bat` |
| Windows, PowerShell | `.venv\Scripts\Activate.ps1` |
| macOS o Linux | `source .venv/bin/activate` |

```text
python -m pip install -r requirements.txt
python calculadora.py
```

## Operaciones y API

La clase `Calculadora` recibe una operación y una lista de números. `resultado()` valida la entrada y selecciona el método correspondiente.

Operaciones: `suma`, `resta`, `multiplicacion`, `division`, `promedio`, `potencia`, `mayor` y `menor`. La potencia requiere exactamente dos números. El menú permite repetir operaciones o salir.

Para iniciar la API:

```text
python -m uvicorn api:aplicacion --host 127.0.0.1 --port 8000
```

| Ruta | Función |
| --- | --- |
| `GET /estado` | Devuelve `{"estado": "correcto"}`. |
| `POST /calcular` | Recibe la operación y sus números. |

Ejemplo de cuerpo JSON para `POST /calcular`:

```json
{"operacion": "promedio", "numeros": [8, 9, 10]}
```

Respuesta esperada: `{"resultado": 9.0}`. El valor numérico 9 es equivalente. La aplicación se exporta como `aplicacion`; el comando debe usar ese nombre. La documentación interactiva está desactivada.

## Comprobar los cambios

```text
python -m ruff check .
python -m ruff format --check .
python -m pytest pruebas/test_calculadora.py -v
python -m pytest pruebas/test_integracion.py -v
python -m pytest --cov --cov-report=term-missing --cov-report=xml
```

La configuración exige un mínimo de 90 % de cobertura combinada de líneas y ramas. Comprueba qué archivos aparecen en la medición: la entrega requiere incluir calculadora, API y herramientas, sin contar las pruebas. Un porcentaje alto no demuestra por sí solo que todos los resultados sean correctos.

## Guía del proyecto

- [Guía editable](GUIA_ALUMNOS.md).
- [Guía en PDF](material/GUIA_ALUMNOS.pdf).
- [Workflow que genera y publica la guía](https://github.com/AlejandraSaldana/actividad-nlp-2/actions/workflows/guia.yml).

Para regenerar el PDF desde la guía editable:

```text
python -m herramientas.guia_pdf
```

El workflow **Guía del proyecto** publica el artefacto `guia-para-alumnos-pdf` en pushes a `main`, PRs con cambios de documentación y ejecuciones manuales. Para descargarlo: Actions, ejecución correspondiente, Artifacts, `guia-para-alumnos-pdf`. Verifica que el commit de la ejecución sea el de tu entrega.

## SonarQube y entrega

Servidor: [sonarqube.lynvera.ai](https://sonarqube.lynvera.ai). Clave configurada: `team02_actividad02`; debe coincidir con la asignada por el docente. `SONAR_TOKEN` se guarda únicamente como secreto de GitHub Actions. Se requiere un User Token con permisos Browse y Execute Analysis sobre el proyecto.

El reporte debe publicarse en el artefacto `sonarqube-report-pdf-json-md`, con `sonarqube.pdf`, `sonarqube.json` y `sonarqube.md`. La guía explica su descarga y el recorrido de CI.

Antes de entregar, confirma una ejecución aprobada de **CI en main**, Quality Gate aprobado y **0 issues** en el escaneo. Un workflow independiente en verde no sustituye esa comprobación. El análisis y el reporte de SonarQube se omiten en los PR según la configuración del proyecto.

Entrega los enlaces al repositorio público, PR y ejecución aprobada de main; `calculadora.py`, `sonarqube.pdf`, la guía y su PDF; y una explicación breve de una prueba propia, un fallo corregido, cobertura e issues. Los resultados deben tomarse de la ejecución final, sin inventar valores pendientes.

## Referencias

Actividad: continuación de la calculadora a las pruebas automáticas, clase 8. Material docente: [proyecto de referencia](https://github.com/felipecastillotecmx/calculadora) y [guía original](https://github.com/felipecastillotecmx/calculadora/blob/main/material/GUIA_ALUMNOS.pdf). La guía de este repositorio adapta las instrucciones a sus archivos, comandos y clave configurada.
