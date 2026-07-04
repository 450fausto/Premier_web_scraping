# Premier League Match Data Scraper

Este proyecto extrae información de partidos de la Premier League desde páginas de Sky Sports.
A partir de una lista de enlaces de partidos, el script entra automáticamente a la sección de estadísticas (`stats`) y equipos (`teams`) para obtener marcador, fecha, equipos, minutos de goles, estadísticas del partido y oficiales.

El resultado se guarda en un archivo CSV llamado:

```text
premier_data.csv
```

---

## Estructura general del archivo

Cada fila del archivo representa un partido.
Las columnas incluyen información general del encuentro, marcador, minutos de goles, estadísticas del partido y enlaces utilizados para la extracción.

---

## Descripción de columnas base

| Columna                   | Descripción                                                                                                                            |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `fecha`                   | Fecha y hora del partido tal como aparece en Sky Sports. Por ejemplo: `8:00pm, Friday 15th August 2025`.                               |
| `local`                   | Nombre del equipo local.                                                                                                               |
| `visitante`               | Nombre del equipo visitante.                                                                                                           |
| `goles_local`             | Número de goles anotados por el equipo local.                                                                                          |
| `goles_visitante`         | Número de goles anotados por el equipo visitante.                                                                                      |
| `goles_totales`           | Suma de los goles del equipo local y visitante.                                                                                        |
| `minutos_goles_local`     | Minutos en los que anotó el equipo local, guardados como texto. Por ejemplo: `37, 49, 88, 94`. Si no anotó goles, queda vacío.         |
| `minutos_goles_visitante` | Minutos en los que anotó el equipo visitante, guardados como texto. Si no anotó goles, queda vacío.                                    |
| `detalle`                 | Texto general del partido extraído del encabezado de Sky Sports. Puede incluir equipos, competición, fecha, estadio y asistencia.      |
| `match_officials`         | Oficiales del partido extraídos de la página de alineaciones/equipos. Puede incluir árbitro, asistentes y otros oficiales disponibles. |
| `url_stats`               | URL de la página de estadísticas utilizada para extraer los datos del partido.                                                         |
| `url_teams`               | URL de la página de equipos o alineaciones utilizada para extraer oficiales y datos complementarios.                                   |

---

## Formato de los minutos de gol

Los minutos de gol se guardan como texto para conservar varios valores dentro de una sola celda.

Ejemplo:

```text
37, 49, 88, 94
```

Reglas aplicadas:

| Caso original | Valor guardado |
| ------------- | -------------- |
| `37'`         | `37`           |
| `49'`         | `49`           |
| `88'`         | `88`           |
| `45+2'`       | `45`           |
| `90+4'`       | `94`           |
| Sin goles     | celda vacía    |

La razón para tratar diferente el agregado del primer tiempo y del segundo tiempo es que un gol al `45+2` se conserva como minuto `45`, mientras que un gol al `90+4` se transforma en `94`.

---

## Columnas de estadísticas

Las estadísticas del partido se generan automáticamente a partir de la información disponible en la página de Sky Sports.
Por eso, el número de columnas puede variar si la página cambia o si algunas estadísticas no están disponibles en ciertos partidos.

Cada estadística se guarda en dos columnas:

```text
nombreEstadistica_H
nombreEstadistica_A
```

Donde:

| Sufijo | Significado                                   |
| ------ | --------------------------------------------- |
| `_H`   | Valor del equipo local, es decir, `home`.     |
| `_A`   | Valor del equipo visitante, es decir, `away`. |

Por ejemplo:

```text
totalScoringAtt_H
totalScoringAtt_A
```

significa:

| Columna             | Descripción                         |
| ------------------- | ----------------------------------- |
| `totalScoringAtt_H` | Tiros totales del equipo local.     |
| `totalScoringAtt_A` | Tiros totales del equipo visitante. |

---

## Estadísticas comunes

A continuación se describen algunas de las estadísticas que pueden aparecer en el archivo CSV.

| Columna base            | Descripción                                                                                                 |
| ----------------------- | ----------------------------------------------------------------------------------------------------------- |
| `expectedGoals`         | Goles esperados, también conocido como xG. Mide la calidad de las ocasiones generadas.                      |
| `expectedGoalsOnTarget` | Goles esperados a puerta, también conocido como xGOT. Considera la calidad de los tiros que fueron al arco. |
| `expectedGoalsConceded` | Goles esperados concedidos. Representa la calidad de las oportunidades permitidas al rival.                 |
| `totalScoringAtt`       | Tiros totales realizados por el equipo.                                                                     |
| `ontargetScoringAtt`    | Tiros a puerta.                                                                                             |
| `shotOffTarget`         | Tiros fuera del arco.                                                                                       |
| `blockedScoringAtt`     | Tiros bloqueados por el rival.                                                                              |
| `bigChanceMissed`       | Grandes ocasiones falladas.                                                                                 |
| `accuratePass`          | Pases acertados.                                                                                            |
| `percentPass`           | Porcentaje de precisión de pase.                                                                            |
| `totalTackle`           | Entradas o tackles totales.                                                                                 |
| `wonTackle`             | Entradas exitosas.                                                                                          |
| `percentTackle`         | Porcentaje de éxito en entradas.                                                                            |
| `woodworkHit`           | Tiros al poste o travesaño.                                                                                 |

Cada una de estas estadísticas puede aparecer con los sufijos `_H` y `_A`.

Ejemplo:

| Columna             | Descripción                                         |
| ------------------- | --------------------------------------------------- |
| `expectedGoals_H`   | xG del equipo local.                                |
| `expectedGoals_A`   | xG del equipo visitante.                            |
| `shotOffTarget_H`   | Tiros fuera del equipo local.                       |
| `shotOffTarget_A`   | Tiros fuera del equipo visitante.                   |
| `bigChanceMissed_H` | Grandes ocasiones falladas por el equipo local.     |
| `bigChanceMissed_A` | Grandes ocasiones falladas por el equipo visitante. |

---

## Interpretación de valores

Los valores extraídos pueden ser enteros, decimales o porcentajes.

| Tipo de valor | Ejemplo | Interpretación                                                                     |
| ------------- | ------- | ---------------------------------------------------------------------------------- |
| Entero        | `19`    | Conteo de eventos, como tiros, pases o faltas.                                     |
| Decimal       | `2.21`  | Valor estimado, como xG.                                                           |
| Porcentaje    | `82`    | Porcentaje, como precisión de pase. El símbolo `%` se elimina durante la limpieza. |
| Texto vacío   | `""`    | Dato no disponible o equipo sin evento registrado.                                 |

---

## Ejemplo de una fila

Una fila del CSV puede representar un partido como:

| fecha                           | local     | visitante   | goles_local | goles_visitante | minutos_goles_local | minutos_goles_visitante |
| ------------------------------- | --------- | ----------- | ----------: | --------------: | ------------------- | ----------------------- |
| 8:00pm, Friday 15th August 2025 | Liverpool | Bournemouth |           4 |               2 | 37, 49, 88, 94      | 64, 76                  |

Y algunas columnas estadísticas podrían verse así:

| totalScoringAtt_H | totalScoringAtt_A | ontargetScoringAtt_H | ontargetScoringAtt_A | shotOffTarget_H | shotOffTarget_A |
| ----------------: | ----------------: | -------------------: | -------------------: | --------------: | --------------: |
|                19 |                10 |                   10 |                    3 |               7 |               4 |

---

## Notas importantes

1. Las columnas estadísticas se generan dinámicamente.
   Si Sky Sports agrega, elimina o renombra estadísticas, el CSV puede cambiar.

2. El sufijo `_H` siempre corresponde al equipo local.
   El sufijo `_A` siempre corresponde al equipo visitante.

3. Los minutos de gol se guardan como texto porque un equipo puede anotar varios goles en un mismo partido.

4. Si un equipo no anota goles, la columna de minutos correspondiente queda vacía.

5. El archivo depende de la estructura HTML de Sky Sports. Si la página cambia, puede ser necesario actualizar los XPath o los `data-testid` utilizados en el script.

---

## Objetivo del dataset

El archivo generado puede utilizarse para análisis estadístico, visualización de datos o desarrollo de modelos predictivos relacionados con partidos de la Premier League.

Algunas posibles aplicaciones son:

* análisis de rendimiento por equipo;
* comparación entre estadísticas ofensivas y defensivas;
* estudio de relación entre tiros a puerta y goles;
* análisis de localía;
* generación de tablas acumuladas por temporada;
* entrenamiento de modelos predictivos para resultados de partidos.
