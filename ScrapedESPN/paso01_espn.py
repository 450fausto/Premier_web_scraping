import requests as rq
from fechas_array import generar_fechas
import pathlib as pl
import csv
import time
import re


# Rango de fechas
array = generar_fechas("20250801", "20260630")


# Headers
hdr = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "es-MX,es;q=0.9,en;q=0.8",
    "Accept": "application/json,text/plain,*/*",
}


URL_SCOREBOARD = "https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard"
URL_SUMMARY = "https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/summary"


def pedir_json(url, params=None):
    ans = rq.get(url, headers=hdr, params=params, timeout=20)

    if ans.status_code != 200:
        raise RuntimeError(f"Error {ans.status_code}: {ans.url}")

    return ans.json()


def obtener_partidos_fecha(fecha):
    """
    Obtiene los partidos de Premier League de una fecha.
    """
    fecha = str(fecha)

    data = pedir_json(
        URL_SCOREBOARD,
        params={"dates": fecha}
    )

    return data.get("events", [])


def obtener_summary(game_id):
    """
    Obtiene el summary de ESPN para un partido.
    """
    data = pedir_json(
        URL_SUMMARY,
        params={"event": str(game_id)}
    )

    return data


def limpiar_numero(valor):
    """
    Convierte valores numéricos si se puede.
    Si no, devuelve el valor original.
    """
    if valor is None:
        return ""

    try:
        if isinstance(valor, str):
            valor = valor.strip()

        if valor == "":
            return ""

        if "." in str(valor):
            num = float(valor)
            if num.is_integer():
                return int(num)
            return num

        return int(valor)

    except Exception:
        return valor


def minuto_espn_a_entero(display_value):
    """
    Convierte minutos ESPN a entero.

    Reglas:
    - "5'"      -> 5
    - "30'"     -> 30
    - "45'+3'"  -> 45
    - "90'+5'"  -> 95

    La lógica especial es:
    - Si hay agregado antes del 90, se conserva sólo el minuto base.
    - Si hay agregado en 90+, se suma el agregado.
    """
    if not display_value:
        return None

    texto = str(display_value).strip()

    patron = r"(\d+)'(?:\+(\d+)')?"
    match = re.search(patron, texto)

    if not match:
        return None

    base = int(match.group(1))
    agregado = match.group(2)

    if agregado is None:
        return base

    agregado = int(agregado)

    if base >= 90:
        return base + agregado

    return base


def minutos_a_string(minutos):
    """
    Convierte lista de minutos a string separado por comas.
    """
    if not minutos:
        return ""

    minutos = [m for m in minutos if m is not None]
    minutos.sort()

    return ", ".join(str(m) for m in minutos)


def extraer_info_scoreboard(evento):
    """
    Extrae fecha, hora, local, visitante y marcador desde scoreboard.
    """
    game_id = evento.get("id", "")

    fecha_hora = evento.get("date", "")
    fecha = ""
    hora = ""

    if fecha_hora:
        # ESPN lo entrega como UTC ISO:
        # 2025-05-04T13:00Z
        fecha = fecha_hora[:10]
        hora = fecha_hora[11:16]

    competitions = evento.get("competitions", [])
    competition = competitions[0] if competitions else {}

    competitors = competition.get("competitors", [])

    local = ""
    visitante = ""
    id_local = ""
    id_visitante = ""
    goles_local = ""
    goles_visitante = ""

    for comp in competitors:
        home_away = comp.get("homeAway")
        team = comp.get("team", {})

        nombre = team.get("displayName", "")
        team_id = team.get("id", "")
        score = comp.get("score", "")

        if home_away == "home":
            local = nombre
            id_local = str(team_id)
            goles_local = limpiar_numero(score)

        elif home_away == "away":
            visitante = nombre
            id_visitante = str(team_id)
            goles_visitante = limpiar_numero(score)

    return {
        "game_id": str(game_id),
        "fecha": fecha,
        "hora": hora,
        "local": local,
        "visitante": visitante,
        "id_local": id_local,
        "id_visitante": id_visitante,
        "goles_local": goles_local,
        "goles_visitante": goles_visitante,
    }


def extraer_minutos_goles(summary, id_local, id_visitante, local, visitante):
    """
    Extrae los minutos en que anotó local y visitante.
    Usa scoringPlay == True en keyEvents.

    En autogoles, ESPN normalmente asigna el gol al equipo beneficiado,
    por eso se usa evento["team"], no el jugador.
    """
    minutos_local = []
    minutos_visitante = []

    for evento in summary.get("keyEvents", []):
        if not evento.get("scoringPlay", False):
            continue

        team = evento.get("team", {})
        team_id = str(team.get("id", ""))
        team_name = team.get("displayName", "")

        clock = evento.get("clock", {})
        minuto = minuto_espn_a_entero(clock.get("displayValue"))

        if team_id == str(id_local) or team_name == local:
            minutos_local.append(minuto)

        elif team_id == str(id_visitante) or team_name == visitante:
            minutos_visitante.append(minuto)

    return {
        "minutos_goles_local": minutos_a_string(minutos_local),
        "minutos_goles_visitante": minutos_a_string(minutos_visitante),
    }


def estadisticas_equipo_a_dict(team_box):
    """
    Convierte la lista de estadísticas de ESPN a diccionario.
    """
    stats = {}

    for stat in team_box.get("statistics", []):
        nombre = stat.get("name")
        valor = stat.get("displayValue")

        if nombre:
            stats[nombre] = limpiar_numero(valor)

    return stats


def extraer_estadisticas(summary):
    """
    Extrae estadísticas de local y visitante desde boxscore.
    """
    salida = {
        "posesion_local": "",
        "posesion_visit": "",
        "tiros_meta_local": "",
        "tiros_meta_visit": "",
        "tiros_local": "",
        "tiros_visit": "",
        "faltas_local": "",
        "faltas_visit": "",
        "amarillas_local": "",
        "amarillas_visit": "",
        "rojas_local": "",
        "rojas_visit": "",
        "cornels_local": "",
        "cornels_visit": "",
        "atajadas_local": "",
        "atajadas_visit": "",
    }

    teams = summary.get("boxscore", {}).get("teams", [])

    for team_box in teams:
        home_away = team_box.get("homeAway")
        stats = estadisticas_equipo_a_dict(team_box)

        if home_away == "home":
            sufijo = "local"
        elif home_away == "away":
            sufijo = "visit"
        else:
            continue

        salida[f"posesion_{sufijo}"] = stats.get("possessionPct", "")
        salida[f"tiros_meta_{sufijo}"] = stats.get("shotsOnTarget", "")
        salida[f"tiros_{sufijo}"] = stats.get("totalShots", "")
        salida[f"faltas_{sufijo}"] = stats.get("foulsCommitted", "")
        salida[f"amarillas_{sufijo}"] = stats.get("yellowCards", "")
        salida[f"rojas_{sufijo}"] = stats.get("redCards", "")
        salida[f"cornels_{sufijo}"] = stats.get("wonCorners", "")
        salida[f"atajadas_{sufijo}"] = stats.get("saves", "")

    return salida


def procesar_partido(evento_scoreboard):
    """
    Procesa un partido completo:
    - datos generales desde scoreboard
    - minutos de goles desde summary
    - estadísticas desde summary
    """
    base = extraer_info_scoreboard(evento_scoreboard)

    game_id = base["game_id"]

    summary = obtener_summary(game_id)

    goles = extraer_minutos_goles(
        summary=summary,
        id_local=base["id_local"],
        id_visitante=base["id_visitante"],
        local=base["local"],
        visitante=base["visitante"],
    )

    stats = extraer_estadisticas(summary)

    fila = {
        "fecha": base["fecha"],
        "hora": base["hora"],
        "local": base["local"],
        "visitante": base["visitante"],
        "goles_local": base["goles_local"],
        "goles_visitante": base["goles_visitante"],
        "minutos_goles_local": goles["minutos_goles_local"],
        "minutos_goles_visitante": goles["minutos_goles_visitante"],
        "posesion_local": stats["posesion_local"],
        "posesion_visit": stats["posesion_visit"],
        "tiros_meta_local": stats["tiros_meta_local"],
        "tiros_meta_visit": stats["tiros_meta_visit"],
        "tiros_local": stats["tiros_local"],
        "tiros_visit": stats["tiros_visit"],
        "faltas_local": stats["faltas_local"],
        "faltas_visit": stats["faltas_visit"],
        "amarillas_local": stats["amarillas_local"],
        "amarillas_visit": stats["amarillas_visit"],
        "rojas_local": stats["rojas_local"],
        "rojas_visit": stats["rojas_visit"],
        "cornels_local": stats["cornels_local"],
        "cornels_visit": stats["cornels_visit"],
        "atajadas_local": stats["atajadas_local"],
        "atajadas_visit": stats["atajadas_visit"],
    }

    return fila


def guardar_csv(datos, nombre_archivo):
    """
    Guarda lista de diccionarios en CSV.
    """
    if not datos:
        print("No hay datos para guardar.")
        return

    columnas = [
        "fecha",
        "hora",
        "local",
        "visitante",
        "goles_local",
        "goles_visitante",
        "minutos_goles_local",
        "minutos_goles_visitante",
        "posesion_local",
        "posesion_visit",
        "tiros_meta_local",
        "tiros_meta_visit",
        "tiros_local",
        "tiros_visit",
        "faltas_local",
        "faltas_visit",
        "amarillas_local",
        "amarillas_visit",
        "rojas_local",
        "rojas_visit",
        "cornels_local",
        "cornels_visit",
        "atajadas_local",
        "atajadas_visit",
    ]

    ruta = pl.Path(nombre_archivo)

    with ruta.open("w", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=columnas)
        writer.writeheader()
        writer.writerows(datos)

    print(f"CSV guardado en: {ruta.resolve()}")


# Programa principal
filas = []
game_ids_vistos = set()

for fecha in array:
    try:
        eventos = obtener_partidos_fecha(fecha)

        if not eventos:
            print(f"{fecha}: sin partidos")
            continue

        print(f"{fecha}: {len(eventos)} partido(s) encontrados")

        for evento in eventos:
            game_id = str(evento.get("id", ""))

            if not game_id or game_id in game_ids_vistos:
                continue

            try:
                fila = procesar_partido(evento)
                filas.append(fila)
                game_ids_vistos.add(game_id)

                print(
                    f"  OK {game_id}: "
                    f"{fila['local']} {fila['goles_local']}-"
                    f"{fila['goles_visitante']} {fila['visitante']}"
                )

                time.sleep(0.5)

            except Exception as e:
                print(f"  Error en partido {game_id}: {e}")

        time.sleep(0.5)

    except Exception as e:
        print(f"Error en fecha {fecha}: {e}")


guardar_csv(
    filas,
    "premier_2025_2026_espn_partidos.csv"
)