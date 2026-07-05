# Premier League ESPN Scraper

Script en Python para construir una base de datos de partidos de la **Premier League** a partir de endpoints JSON de ESPN.

El objetivo principal es obtener, por partido, información general, marcador, minutos de goles y estadísticas básicas de ambos equipos.

---

## Descripción

Este proyecto consulta información histórica de partidos de la Premier League usando los endpoints JSON de ESPN.

A diferencia de un scraper basado en HTML, este enfoque no depende de XPath ni de la estructura visual de la página. En lugar de eso, utiliza directamente la información JSON asociada a cada partido.

El script obtiene:

* Fecha y hora del partido.
* Equipo local y visitante.
* Marcador final.
* Minutos en los que anotó cada equipo.
* Posesión.
* Tiros totales.
* Tiros a puerta.
* Faltas.
* Tarjetas amarillas.
* Tarjetas rojas.
* Corners.
* Atajadas.

El resultado final se guarda en un archivo `.csv`.

---

## Fuente de datos

El script usa dos endpoints de ESPN:

```text
https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard
```

Este endpoint se usa para obtener los partidos de una fecha específica.

```text
https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/summary
```

Este endpoint se usa para obtener el detalle de cada partido mediante su `game_id`.

---

## Estructura general del proceso

El flujo del programa es:

```text
Rango de fechas
↓
Consulta al scoreboard de ESPN
↓
Obtención de game_id por partido
↓
Consulta al summary de cada partido
↓
Extracción de goles y estadísticas
↓
Construcción de filas
↓
Exportación a CSV
```

---

## Requisitos

Se requiere Python 3.10 o superior.

Librerías utilizadas:

```python
requests
pathlib
csv
time
re
```

También se utiliza una función externa llamada `generar_fechas`, ubicada en el archivo:

```text
fechas_array.py
```

---

## Instalación

Crear y activar un entorno virtual:

```bash
python3 -m venv env
source env/bin/activate
```

Instalar `requests`:

```bash
pip install requests
```

---

## Archivo auxiliar: `fechas_array.py`

El proyecto usa una función para generar fechas en formato `YYYYMMDD`.

Ejemplo de archivo `fechas_array.py`:

```python
from datetime import datetime, timedelta


def generar_fechas(inicio, fin):
    """
    Genera una lista de fechas en formato YYYYMMDD desde inicio hasta fin.

    Parámetros
    ----------
    inicio : str o int
        Fecha inicial en formato YYYYMMDD.
    fin : str o int
        Fecha final en formato YYYYMMDD.

    Retorna
    -------
    list
        Lista de fechas en formato int YYYYMMDD.
    """
    inicio = datetime.strptime(str(inicio), "%Y%m%d")
    fin = datetime.strptime(str(fin), "%Y%m%d")

    fechas = []
    fecha_actual = inicio

    while fecha_actual <= fin:
        fechas.append(int(fecha_actual.strftime("%Y%m%d")))
        fecha_actual += timedelta(days=1)

    return fechas
```

---

## Uso

En el script principal se define el rango de fechas:

```python
array = generar_fechas("20240801", "20250530")
```

Este rango corresponde aproximadamente a la temporada 2024-2025 de la Premier League.

Después se ejecuta el script:

```bash
python scraper_premier_espn.py
```

Al finalizar, se genera un archivo CSV:

```text
premier_2024_2025_espn_partidos.csv
```

---

## Columnas del CSV

El archivo generado contiene las siguientes columnas:

| Columna                   | Descripción                                                       |
| ------------------------- | ----------------------------------------------------------------- |
| `fecha`                   | Fecha del partido en formato `YYYY-MM-DD`.                        |
| `hora`                    | Hora del partido tomada del campo horario de ESPN.                |
| `local`                   | Equipo local.                                                     |
| `visitante`               | Equipo visitante.                                                 |
| `goles_local`             | Goles anotados por el equipo local.                               |
| `goles_visitante`         | Goles anotados por el equipo visitante.                           |
| `minutos_goles_local`     | Minutos en los que anotó el equipo local, separados por coma.     |
| `minutos_goles_visitante` | Minutos en los que anotó el equipo visitante, separados por coma. |
| `posesion_local`          | Porcentaje de posesión del equipo local.                          |
| `posesion_visit`          | Porcentaje de posesión del equipo visitante.                      |
| `tiros_meta_local`        | Tiros a puerta del equipo local.                                  |
| `tiros_meta_visit`        | Tiros a puerta del equipo visitante.                              |
| `tiros_local`             | Tiros totales del equipo local.                                   |
| `tiros_visit`             | Tiros totales del equipo visitante.                               |
| `faltas_local`            | Faltas cometidas por el equipo local.                             |
| `faltas_visit`            | Faltas cometidas por el equipo visitante.                         |
| `amarillas_local`         | Tarjetas amarillas del equipo local.                              |
| `amarillas_visit`         | Tarjetas amarillas del equipo visitante.                          |
| `rojas_local`             | Tarjetas rojas del equipo local.                                  |
| `rojas_visit`             | Tarjetas rojas del equipo visitante.                              |
| `cornels_local`           | Corners del equipo local.                                         |
| `cornels_visit`           | Corners del equipo visitante.                                     |
| `atajadas_local`          | Atajadas del equipo local.                                        |
| `atajadas_visit`          | Atajadas del equipo visitante.                                    |

---

## Formato de los minutos de gol

Los minutos de gol se guardan como texto, separados por comas.

Ejemplo:

```text
5, 30, 72
```

Si un equipo no anotó goles, el campo queda vacío:

```text
```

### Casos con tiempo agregado

El script aplica las siguientes reglas:

| Minuto ESPN | Minuto guardado |
| ----------- | --------------- |
| `14'`       | `14`            |
| `45'+3'`    | `45`            |
| `90'+5'`    | `95`            |

Es decir:

* En tiempo agregado del primer tiempo, se conserva sólo el minuto base.
* En tiempo agregado posterior al minuto 90, se suma el agregado.

---

## Tratamiento de autogoles

Para los autogoles, el minuto se asigna al equipo que recibió el gol en el marcador.

Por ejemplo, si un jugador visitante anota autogol a favor del equipo local, el minuto se guarda en:

```text
minutos_goles_local
```

Esto se hace porque el objetivo de la base es modelar el comportamiento del marcador, no la autoría individual del gol.

---

## Notas importantes

La hora devuelta por ESPN suele venir en formato UTC dentro del JSON. Si se requiere hora local de México u otra zona horaria, debe agregarse una conversión horaria.

El script evita scrapear directamente el HTML de ESPN porque la página puede activar verificaciones anti-bot o modificar su estructura visual. El uso del endpoint JSON es más estable para este caso.

Algunas estadísticas pueden no aparecer en partidos muy antiguos, suspendidos, cancelados o sin cobertura completa. En esos casos, el campo queda vacío.

---

## Posibles mejoras

Algunas mejoras futuras podrían ser:

* Convertir la hora UTC a hora local.
* Agregar `game_id` como columna de control.
* Guardar también los nombres de los goleadores.
* Guardar asistencias.
* Separar goles normales, penales y autogoles.
* Convertir la base a formato largo, con una fila por gol.
* Integrar varias temporadas en un solo CSV.
* Cruzar esta base con datos de `football-data.co.uk`.

---

## Salida esperada

Ejemplo de fila en el CSV:

```text
fecha,hora,local,visitante,goles_local,goles_visitante,minutos_goles_local,minutos_goles_visitante,posesion_local,posesion_visit,tiros_meta_local,tiros_meta_visit,tiros_local,tiros_visit,faltas_local,faltas_visit,amarillas_local,amarillas_visit,rojas_local,rojas_visit,cornels_local,cornels_visit,atajadas_local,atajadas_visit
2025-05-04,13:00,Brentford,Manchester United,4,3,"27, 33, 70, 74","14, 82, 95",46.8,53.2,6,5,12,14,8,10,0,2,0,0,7,4,2,3
```

---

## Estado del proyecto

El proyecto permite construir una base de datos útil para análisis estadístico y modelos predictivos de partidos de fútbol, especialmente cuando se desea incluir información temporal de los goles, una variable que no suele aparecer en bases de datos tradicionales.
