# Base de datos de partidos de Premier League

Esta base de datos contiene información de partidos de la **Premier League** obtenida a partir de endpoints JSON de ESPN.

Cada fila representa un partido y contiene datos generales, marcador final, minutos de goles y estadísticas básicas de ambos equipos.

---

## Descripción general

La base fue construida con el objetivo de reunir información útil para análisis estadístico y modelos predictivos de fútbol.

Una característica importante de esta base es que incluye los **minutos en los que se anotaron los goles**, dato que no suele encontrarse fácilmente en bases de datos tradicionales de resultados deportivos.

Además, se incluyen estadísticas del partido como posesión, tiros, tiros a puerta, faltas, tarjetas, corners y atajadas.

---

## Unidad de observación

Cada fila de la base representa un partido.

Por lo tanto, la unidad de análisis es:

```text
Un partido de Premier League
```

---

## Formato del archivo

La base se encuentra en formato `.csv`.

Archivo generado:

```text
premier_2024_2025_espn_partidos.csv
```

---

## Diccionario de variables

| Variable                  | Tipo sugerido | Descripción                                                        |
| ------------------------- | ------------: | ------------------------------------------------------------------ |
| `fecha`                   | texto / fecha | Fecha del partido en formato `YYYY-MM-DD`.                         |
| `hora`                    |  texto / hora | Hora del partido tomada del registro de ESPN.                      |
| `local`                   |         texto | Nombre del equipo local.                                           |
| `visitante`               |         texto | Nombre del equipo visitante.                                       |
| `goles_local`             |        entero | Número de goles anotados por el equipo local.                      |
| `goles_visitante`         |        entero | Número de goles anotados por el equipo visitante.                  |
| `minutos_goles_local`     |         texto | Minutos en los que anotó el equipo local, separados por comas.     |
| `minutos_goles_visitante` |         texto | Minutos en los que anotó el equipo visitante, separados por comas. |
| `posesion_local`          |      numérico | Porcentaje de posesión del equipo local.                           |
| `posesion_visit`          |      numérico | Porcentaje de posesión del equipo visitante.                       |
| `tiros_meta_local`        |        entero | Tiros a puerta realizados por el equipo local.                     |
| `tiros_meta_visit`        |        entero | Tiros a puerta realizados por el equipo visitante.                 |
| `tiros_local`             |        entero | Tiros totales realizados por el equipo local.                      |
| `tiros_visit`             |        entero | Tiros totales realizados por el equipo visitante.                  |
| `faltas_local`            |        entero | Faltas cometidas por el equipo local.                              |
| `faltas_visit`            |        entero | Faltas cometidas por el equipo visitante.                          |
| `amarillas_local`         |        entero | Tarjetas amarillas recibidas por el equipo local.                  |
| `amarillas_visit`         |        entero | Tarjetas amarillas recibidas por el equipo visitante.              |
| `rojas_local`             |        entero | Tarjetas rojas recibidas por el equipo local.                      |
| `rojas_visit`             |        entero | Tarjetas rojas recibidas por el equipo visitante.                  |
| `cornels_local`           |        entero | Tiros de esquina obtenidos por el equipo local.                    |
| `cornels_visit`           |        entero | Tiros de esquina obtenidos por el equipo visitante.                |
| `atajadas_local`          |        entero | Atajadas realizadas por el equipo local.                           |
| `atajadas_visit`          |        entero | Atajadas realizadas por el equipo visitante.                       |

---

## Variables de identificación del partido

### `fecha`

Indica la fecha en la que se jugó el partido.

Ejemplo:

```text
2025-05-04
```

---

### `hora`

Indica la hora registrada para el partido.

Ejemplo:

```text
13:00
```

Nota: la hora proviene del registro original de ESPN. Dependiendo del endpoint consultado, puede ser necesario verificar si corresponde a UTC o a una zona horaria local.

---

### `local`

Equipo que aparece como local en el partido.

Ejemplo:

```text
Brentford
```

---

### `visitante`

Equipo que aparece como visitante en el partido.

Ejemplo:

```text
Manchester United
```

---

## Variables de marcador

### `goles_local`

Número total de goles anotados por el equipo local.

Ejemplo:

```text
4
```

---

### `goles_visitante`

Número total de goles anotados por el equipo visitante.

Ejemplo:

```text
3
```

---

## Variables de minutos de gol

### `minutos_goles_local`

Contiene los minutos en los que anotó el equipo local.

Los valores se guardan como texto, separados por comas.

Ejemplo:

```text
27, 33, 70, 74
```

Si el equipo local no anotó goles, el campo queda vacío:

```text
```

---

### `minutos_goles_visitante`

Contiene los minutos en los que anotó el equipo visitante.

Los valores se guardan como texto, separados por comas.

Ejemplo:

```text
14, 82, 95
```

Si el equipo visitante no anotó goles, el campo queda vacío:

```text
```

---

## Regla para minutos en tiempo agregado

Los minutos con tiempo agregado se transformaron siguiendo una regla específica.

| Registro original | Valor guardado |
| ----------------- | -------------: |
| `45+1`            |           `45` |
| `45+2`            |           `45` |
| `45+3`            |           `45` |
| `90+1`            |           `91` |
| `90+2`            |           `92` |
| `90+5`            |           `95` |

Es decir:

* Si el gol ocurre en tiempo agregado del primer tiempo, se conserva sólo el minuto base `45`.
* Si el gol ocurre en tiempo agregado después del minuto `90`, se suma el agregado.

Por ejemplo:

```text
90+5 → 95
```

---

## Tratamiento de autogoles

Los autogoles se asignan al equipo que recibió el gol en el marcador.

Por ejemplo, si un jugador del equipo visitante anota autogol a favor del equipo local, ese minuto se registra en:

```text
minutos_goles_local
```

Esto permite que las columnas de minutos de gol representen correctamente la evolución del marcador del partido.

---

## Variables estadísticas del partido

### `posesion_local`

Porcentaje de posesión del equipo local.

Ejemplo:

```text
46.8
```

---

### `posesion_visit`

Porcentaje de posesión del equipo visitante.

Ejemplo:

```text
53.2
```

La suma de ambas posesiones debería ser cercana a `100`, salvo posibles redondeos.

---

### `tiros_meta_local`

Número de tiros a puerta realizados por el equipo local.

Ejemplo:

```text
6
```

---

### `tiros_meta_visit`

Número de tiros a puerta realizados por el equipo visitante.

Ejemplo:

```text
5
```

---

### `tiros_local`

Número total de tiros realizados por el equipo local.

Ejemplo:

```text
12
```

---

### `tiros_visit`

Número total de tiros realizados por el equipo visitante.

Ejemplo:

```text
14
```

---

### `faltas_local`

Número de faltas cometidas por el equipo local.

Ejemplo:

```text
8
```

---

### `faltas_visit`

Número de faltas cometidas por el equipo visitante.

Ejemplo:

```text
10
```

---

### `amarillas_local`

Número de tarjetas amarillas recibidas por el equipo local.

Ejemplo:

```text
0
```

---

### `amarillas_visit`

Número de tarjetas amarillas recibidas por el equipo visitante.

Ejemplo:

```text
2
```

---

### `rojas_local`

Número de tarjetas rojas recibidas por el equipo local.

Ejemplo:

```text
0
```

---

### `rojas_visit`

Número de tarjetas rojas recibidas por el equipo visitante.

Ejemplo:

```text
0
```

---

### `cornels_local`

Número de tiros de esquina obtenidos por el equipo local.

Ejemplo:

```text
7
```

Nota: el nombre de la variable conserva la forma `cornels`, aunque conceptualmente corresponde a `corners`.

---

### `cornels_visit`

Número de tiros de esquina obtenidos por el equipo visitante.

Ejemplo:

```text
4
```

Nota: el nombre de la variable conserva la forma `cornels`, aunque conceptualmente corresponde a `corners`.

---

### `atajadas_local`

Número de atajadas realizadas por el equipo local.

Ejemplo:

```text
2
```

---

### `atajadas_visit`

Número de atajadas realizadas por el equipo visitante.

Ejemplo:

```text
3
```

---

## Ejemplo de fila

Una fila de la base puede verse así:

```text
fecha,hora,local,visitante,goles_local,goles_visitante,minutos_goles_local,minutos_goles_visitante,posesion_local,posesion_visit,tiros_meta_local,tiros_meta_visit,tiros_local,tiros_visit,faltas_local,faltas_visit,amarillas_local,amarillas_visit,rojas_local,rojas_visit,cornels_local,cornels_visit,atajadas_local,atajadas_visit
2025-05-04,13:00,Brentford,Manchester United,4,3,"27, 33, 70, 74","14, 82, 95",46.8,53.2,6,5,12,14,8,10,0,2,0,0,7,4,2,3
```

---

## Consideraciones para análisis

Las columnas `minutos_goles_local` y `minutos_goles_visitante` están almacenadas como texto. Si se desea hacer análisis numérico con ellas, será necesario separarlas y convertirlas a listas de enteros.

Por ejemplo:

```python
"5, 30, 72" → [5, 30, 72]
```

Para algunos modelos estadísticos, puede ser conveniente transformar estas columnas en nuevas variables, por ejemplo:

* Primer minuto de gol local.
* Primer minuto de gol visitante.
* Último minuto de gol local.
* Último minuto de gol visitante.
* Número de goles en el primer tiempo.
* Número de goles en el segundo tiempo.
* Diferencia de goles al descanso.
* Goles anotados después del minuto 75.
* Tiempo transcurrido hasta el primer gol.

---

## Posibles variables derivadas

A partir de esta base se pueden construir variables adicionales como:

| Variable derivada        | Descripción                                                   |
| ------------------------ | ------------------------------------------------------------- |
| `diferencia_goles`       | Goles local menos goles visitante.                            |
| `resultado`              | Victoria local, empate o victoria visitante.                  |
| `total_goles`            | Suma de goles local y visitante.                              |
| `total_tiros`            | Suma de tiros de ambos equipos.                               |
| `total_tiros_meta`       | Suma de tiros a puerta de ambos equipos.                      |
| `efectividad_local`      | Goles local divididos entre tiros a puerta local.             |
| `efectividad_visit`      | Goles visitante divididos entre tiros a puerta visitante.     |
| `dominio_posesion_local` | Posesión local menos posesión visitante.                      |
| `presion_ofensiva_local` | Combinación de tiros, tiros a puerta y corners del local.     |
| `presion_ofensiva_visit` | Combinación de tiros, tiros a puerta y corners del visitante. |

---

## Limitaciones

La base depende de la disponibilidad y consistencia de los datos publicados por ESPN.

Algunos partidos podrían tener información incompleta si el endpoint no contiene todas las estadísticas o eventos del partido.

La variable `hora` puede requerir ajuste de zona horaria antes de usarse en análisis temporales.

Los minutos de gol se guardan en formato resumido, por lo que no se conserva el detalle original del tiempo agregado salvo en casos posteriores al minuto 90.

---

## Uso recomendado

Esta base puede utilizarse para:

* Análisis exploratorio de partidos.
* Comparación de rendimiento local y visitante.
* Modelos predictivos de resultado.
* Modelos de goles esperados a partir de estadísticas simples.
* Análisis de momentos de anotación.
* Evaluación de rachas ofensivas y defensivas.
* Cruce con otras bases de resultados históricos.

---

## Estado de la base

La base generada contiene información estructurada de partidos de Premier League y está preparada para ser utilizada en análisis estadístico o como insumo para modelos de predicción deportiva.
