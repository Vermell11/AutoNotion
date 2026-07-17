"""Informe diario o semanal, compacto y visual, a partir de actividades de Notion."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any
import unicodedata

from .excel_export import property_value
from .notion_client import NotionClient


class WeeklyReportError(RuntimeError):
    """El informe no pudo generarse."""


@dataclass(frozen=True)
class Activity:
    title: str
    reported_on: date
    status: str
    category: str
    module: str
    hours: float


@dataclass(frozen=True)
class WeeklyReportResult:
    output: Path
    start: date
    end: date
    activities: int
    hours: float
    period: str = "semanal"
    scope: str = "trabajo"


DEFAULT_FIELDS = {
    "title": "Titulo",
    "date": "Date Reported",
    "status": "Status",
    "category": "Category",
    "module": "Modulo",
    "hours": "Horas",
}

DONE_STATUSES = {
    "cerrado",
    "completado",
    "done",
    "finalizado",
    "resolved",
    "resuelto",
    "terminado",
}

PERIODS = ("diario", "semanal")
SCOPES = ("trabajo", "personal", "todo")
PERSONAL_CATEGORY = "personal"

# Tipos de trabajo derivados de la data:
# - Reuniones: la categoría o el título empiezan por "Reunión".
# - Desarrollo: categoría "Desarrollo" o, como heurística, estado "Cerrado"
#   (solo actividades con cambios de código).
# - Gestión: el resto (tareas manuales). El nombre difiere a propósito de la
#   categoría "Operativo" de Notion para no mezclar taxonomías en el reporte.
TYPE_MEETINGS = "Reuniones"
TYPE_CODE = "Desarrollo"
TYPE_OPERATIONS = "Gestión"

# Ventana hacia atrás para buscar asuntos abiertos de periodos anteriores.
OPEN_LOOKBACK_DAYS = 90

# Tema claro ejecutivo: fondo blanco, texto tinta, acentos azul/cian.
PAGE_SIZE = (960, 540)
BG = "#FDFEFF"
INK = "#10233F"
SLATE = "#54677F"
FAINT = "#8CA0B8"
BLUE = "#0B5FD9"
CYAN = "#0FB5CE"
VIOLET = "#6C5CE7"
GRAY = "#9AA9BC"
BORDER = "#DFE7F1"
TRACK = "#EAF0F7"
ZEBRA = "#F5F8FC"

# Pills de estado: fondo tenue y texto oscuro del mismo matiz.
STATUS_STYLES = {
    "resuelto": ("#E5F4EA", "#1E7E34"),
    "cerrado": ("#E8F0FE", "#0B5FD9"),
    "en progreso": ("#FEF3C7", "#92400E"),
    "en curso": ("#FEF3C7", "#92400E"),
    "sin empezar": ("#FDE8E8", "#B42318"),
}
STATUS_DEFAULT = ("#EEF2F7", "#54677F")

TYPE_COLORS = {
    TYPE_MEETINGS: BLUE,
    TYPE_OPERATIONS: CYAN,
    TYPE_CODE: VIOLET,
}

SCOPE_LABELS = {
    "trabajo": "Ámbito laboral",
    "personal": "Ámbito personal",
    "todo": "Ámbito completo",
}


def week_bounds(reference: date | None = None) -> tuple[date, date]:
    reference = reference or date.today()
    start = reference - timedelta(days=reference.weekday())
    return start, start + timedelta(days=6)


def period_bounds(reference: date | None = None, period: str = "semanal") -> tuple[date, date]:
    """Límites del informe: el día de referencia o su semana (lunes a domingo)."""
    if period not in PERIODS:
        raise WeeklyReportError(f"Periodo inválido: {period}. Usa uno de {PERIODS}.")
    reference = reference or date.today()
    if period == "diario":
        return reference, reference
    return week_bounds(reference)


def generate_weekly_report(
    client: NotionClient,
    *,
    data_source_id: str,
    output: Path,
    reference: date | None = None,
    fields: dict[str, str] | None = None,
    author: str = "Andrés Ortega",
    period: str = "semanal",
    scope: str = "trabajo",
) -> WeeklyReportResult:
    if scope not in SCOPES:
        raise WeeklyReportError(f"Ámbito inválido: {scope}. Usa uno de {SCOPES}.")
    start, end = period_bounds(reference, period)
    activities = load_weekly_activities(
        client,
        data_source_id=data_source_id,
        start=start,
        end=end,
        fields=fields,
        scope=scope,
    )
    span = timedelta(days=(end - start).days + 1)
    previous = load_weekly_activities(
        client,
        data_source_id=data_source_id,
        start=start - span,
        end=start - timedelta(days=1),
        fields=fields,
        scope=scope,
    )
    open_activities = load_open_activities(
        client, data_source_id=data_source_id, end=end, fields=fields, scope=scope
    )
    write_weekly_pdf(
        output,
        activities,
        start=start,
        end=end,
        author=author,
        period=period,
        scope=scope,
        previous=previous,
        open_activities=open_activities,
    )
    return WeeklyReportResult(
        output=output.resolve(),
        start=start,
        end=end,
        activities=len(activities),
        hours=sum(item.hours for item in activities),
        period=period,
        scope=scope,
    )


def load_weekly_activities(
    client: NotionClient,
    *,
    data_source_id: str,
    start: date,
    end: date,
    fields: dict[str, str] | None = None,
    scope: str = "todo",
) -> list[Activity]:
    names = DEFAULT_FIELDS | (fields or {})
    schema = client.retrieve_data_source(data_source_id)
    properties_schema = schema.get("properties", {})
    available = set(properties_schema)
    required = {names["title"], names["date"]}
    missing = sorted(required - available)
    if missing:
        raise WeeklyReportError(
            "Faltan propiedades requeridas en Notion: " + ", ".join(missing)
        )

    query_filter = None
    if properties_schema.get(names["date"], {}).get("type") == "date":
        query_filter = {
            "and": [
                {"property": names["date"], "date": {"on_or_after": start.isoformat()}},
                {"property": names["date"], "date": {"on_or_before": end.isoformat()}},
            ]
        }

    activities: list[Activity] = []
    for page in client.query_data_source(data_source_id, query_filter=query_filter):
        properties = page.get("properties", {})
        reported_on = _as_date(_value(properties, names["date"]))
        if reported_on is None or not start <= reported_on <= end:
            continue
        category = _text(_value(properties, names["category"])) or "Sin categoría"
        module = _text(_value(properties, names["module"])) or "Sin módulo"
        is_personal = PERSONAL_CATEGORY in (_normalize(category), _normalize(module))
        if (scope == "trabajo" and is_personal) or (scope == "personal" and not is_personal):
            continue
        activities.append(
            Activity(
                title=_text(_value(properties, names["title"])) or "(sin título)",
                reported_on=reported_on,
                status=_text(_value(properties, names["status"])) or "Sin estado",
                category=category,
                module=module,
                hours=_hours(_value(properties, names["hours"])),
            )
        )
    return sorted(activities, key=lambda item: (item.reported_on, item.title.casefold()))


def load_open_activities(
    client: NotionClient,
    *,
    data_source_id: str,
    end: date,
    fields: dict[str, str] | None = None,
    scope: str = "todo",
) -> list[Activity]:
    """Actividades sin resolver reportadas hasta `end`, incluso de periodos previos."""
    items = load_weekly_activities(
        client,
        data_source_id=data_source_id,
        start=end - timedelta(days=OPEN_LOOKBACK_DAYS),
        end=end,
        fields=fields,
        scope=scope,
    )
    return [item for item in items if not _is_done(item.status)]


def work_type(item: Activity) -> str:
    """Clasifica la actividad en Reuniones, Desarrollo (código) o Gestión."""
    if _normalize(item.category).startswith("reunion") or _normalize(item.title).startswith(
        "reunion"
    ):
        return TYPE_MEETINGS
    if _normalize(item.category) == "desarrollo" or _normalize(item.status) == "cerrado":
        return TYPE_CODE
    return TYPE_OPERATIONS


def write_weekly_pdf(
    output: Path,
    activities: list[Activity],
    *,
    start: date,
    end: date,
    author: str,
    period: str = "semanal",
    scope: str = "trabajo",
    previous: list[Activity] | None = None,
    open_activities: list[Activity] | None = None,
) -> None:
    canvas_module, colors, simple_split = _reportlab()
    output.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas_module.Canvas(str(output), pagesize=PAGE_SIZE)
    pdf.setTitle(f"Informe {period} {start.isoformat()} - {end.isoformat()}")
    pdf.setAuthor(author)

    _cover(pdf, activities, start, end, author, colors, period, scope, previous)
    _dashboard(pdf, activities, start, end, colors, period)
    _highlights(pdf, activities, start, end, colors, simple_split, period, open_activities)
    _details(pdf, activities, start, end, colors, simple_split, period)
    pdf.save()


def _hours_by_type(activities: list[Activity]) -> dict[str, float]:
    totals = {TYPE_MEETINGS: 0.0, TYPE_OPERATIONS: 0.0, TYPE_CODE: 0.0}
    for item in activities:
        totals[work_type(item)] += item.hours
    return totals


def _cover(
    pdf: Any,
    activities: list[Activity],
    start: date,
    end: date,
    author: str,
    colors: Any,
    period: str,
    scope: str,
    previous: list[Activity] | None = None,
) -> None:
    _background(pdf, colors)
    pdf.setFillColor(colors.HexColor(BLUE))
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(54, 466, "R E P O R T E   D E   G E S T I Ó N")
    pdf.setFillColor(colors.HexColor(CYAN))
    pdf.rect(54, 452, 46, 4, fill=1, stroke=0)

    pdf.setFillColor(colors.HexColor(INK))
    pdf.setFont("Helvetica-Bold", 42)
    pdf.drawString(52, 392, f"Informe {period}")
    pdf.setFillColor(colors.HexColor(SLATE))
    pdf.setFont("Helvetica", 19)
    pdf.drawString(54, 356, _range_label(start, end))
    pdf.setFillColor(colors.HexColor(FAINT))
    pdf.setFont("Helvetica", 12)
    pdf.drawString(54, 326, f"{SCOPE_LABELS[scope]} · Avances, dedicación y focos")
    pdf.drawString(54, 306, author)

    total = len(activities)
    done = sum(_is_done(item.status) for item in activities)
    hours = sum(item.hours for item in activities)
    by_type = _hours_by_type(activities)
    meetings = by_type[TYPE_MEETINGS]
    operations = by_type[TYPE_OPERATIONS]
    code = by_type[TYPE_CODE]
    meeting_share = round(100 * meetings / hours) if hours else 0

    hours_hint = "registradas en el periodo"
    meetings_hint = f"{meeting_share}% del tiempo"
    if previous:
        previous_hours = sum(item.hours for item in previous)
        delta = hours - previous_hours
        hours_hint = f"{'+' if delta >= 0 else ''}{_number(delta)} h vs periodo previo"
        if previous_hours:
            previous_meetings = _hours_by_type(previous)[TYPE_MEETINGS]
            meetings_hint += f" (previo: {round(100 * previous_meetings / previous_hours)}%)"
    cards = [
        ("ACTIVIDADES", str(total), f"{done} resueltas · {total - done} abiertas"),
        ("HORAS", _number(hours), hours_hint),
        ("REUNIONES", f"{_number(meetings)} h", meetings_hint),
        ("DESARROLLO", f"{_number(code)} h", f"gestión: {_number(operations)} h"),
    ]
    for index, (label, value, hint) in enumerate(cards):
        x = 54 + index * 218
        _metric_card(pdf, x, 92, 200, 118, label, value, hint, colors)

    pdf.setStrokeColor(colors.HexColor(TRACK))
    pdf.setLineWidth(12)
    pdf.circle(822, 398, 84, fill=0, stroke=1)
    pdf.setStrokeColor(colors.HexColor(BORDER))
    pdf.setLineWidth(4)
    pdf.circle(822, 398, 52, fill=0, stroke=1)
    pdf.setFillColor(colors.HexColor(CYAN))
    pdf.circle(822, 398, 8, fill=1, stroke=0)
    _footer(pdf, start, end, 1, colors, period)
    pdf.showPage()


def _dashboard(
    pdf: Any, activities: list[Activity], start: date, end: date, colors: Any, period: str
) -> None:
    _background(pdf, colors)
    _page_title(pdf, "Resumen ejecutivo", "¿En qué se fue el tiempo?", colors)

    hours_by_module: dict[str, float] = {}
    for item in activities:
        hours_by_module[item.module] = hours_by_module.get(item.module, 0.0) + item.hours

    _panel(pdf, 48, 232, 414, 190, colors)
    _panel(pdf, 486, 232, 426, 190, colors)
    _panel(pdf, 48, 64, 864, 150, colors)

    _donut(pdf, 48, 232, 414, 190, _hours_by_type(activities), colors)
    _hours_bars(
        pdf,
        508,
        252,
        382,
        140,
        "Horas por módulo",
        _grouped_hours(hours_by_module),
        colors,
    )
    if period == "diario":
        hours_by_activity = {}
        for item in activities:
            hours_by_activity[item.title] = hours_by_activity.get(item.title, 0.0) + item.hours
        _hours_bars(
            pdf,
            72,
            84,
            816,
            110,
            "Horas por actividad",
            _grouped_hours(hours_by_activity, max_items=3),
            colors,
            label_width=280,
        )
    else:
        daily_hours = {
            start + timedelta(days=index): sum(
                item.hours
                for item in activities
                if item.reported_on == start + timedelta(days=index)
            )
            for index in range(7)
        }
        _daily_chart(pdf, 72, 86, 816, 100, daily_hours, colors)
    _footer(pdf, start, end, 2, colors, period)
    pdf.showPage()


def _highlights(
    pdf: Any,
    activities: list[Activity],
    start: date,
    end: date,
    colors: Any,
    simple_split: Any,
    period: str,
    open_activities: list[Activity] | None = None,
) -> None:
    _background(pdf, colors)
    label = "semana" if period == "semanal" else "jornada"
    _page_title(pdf, f"Lectura de la {label}", "Resultados y asuntos abiertos", colors)
    done = sorted(
        (item for item in activities if _is_done(item.status)),
        key=lambda item: (-item.hours, item.reported_on),
    )
    if open_activities is None:
        open_activities = [item for item in activities if not _is_done(item.status)]
    open_items = sorted(open_activities, key=lambda item: item.reported_on)
    _list_panel(
        pdf,
        48,
        90,
        414,
        350,
        "Avances principales",
        done[:6],
        colors,
        simple_split,
        empty="No hay actividades resueltas en el periodo.",
    )
    _list_panel(
        pdf,
        486,
        90,
        426,
        350,
        "Focos en curso",
        open_items[:6],
        colors,
        simple_split,
        empty="No hay asuntos abiertos.",
    )
    _footer(pdf, start, end, 3, colors, period)
    pdf.showPage()


def _details(
    pdf: Any,
    activities: list[Activity],
    start: date,
    end: date,
    colors: Any,
    simple_split: Any,
    period: str,
) -> None:
    chunks = [activities[index : index + 10] for index in range(0, len(activities), 10)] or [[]]
    page = 4
    for chunk_index, chunk in enumerate(chunks, start=1):
        _background(pdf, colors, decorated=False)
        subtitle = "Detalle de actividades"
        if len(chunks) > 1:
            subtitle += f" - {chunk_index} de {len(chunks)}"
        _page_title(pdf, f"Trazabilidad {period}", subtitle, colors)
        _table(pdf, 48, 98, chunk, colors, simple_split)
        _footer(pdf, start, end, page, colors, period)
        pdf.showPage()
        page += 1


def _background(pdf: Any, colors: Any, decorated: bool = True) -> None:
    pdf.setFillColor(colors.HexColor(BG))
    pdf.rect(0, 0, *PAGE_SIZE, fill=1, stroke=0)
    pdf.setFillColor(colors.HexColor(BLUE))
    pdf.rect(0, PAGE_SIZE[1] - 6, PAGE_SIZE[0], 6, fill=1, stroke=0)
    pdf.setFillColor(colors.HexColor(CYAN))
    pdf.rect(0, PAGE_SIZE[1] - 6, 240, 6, fill=1, stroke=0)


def _page_title(pdf: Any, title: str, subtitle: str, colors: Any) -> None:
    pdf.setFillColor(colors.HexColor(INK))
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawString(48, 488, title)
    pdf.setFillColor(colors.HexColor(SLATE))
    pdf.setFont("Helvetica", 13)
    pdf.drawString(48, 464, subtitle)
    pdf.setFillColor(colors.HexColor(CYAN))
    pdf.rect(48, 450, 46, 4, fill=1, stroke=0)


def _metric_card(
    pdf: Any,
    x: float,
    y: float,
    width: float,
    height: float,
    label: str,
    value: str,
    hint: str,
    colors: Any,
) -> None:
    pdf.setFillColor(colors.white)
    pdf.setStrokeColor(colors.HexColor(BORDER))
    pdf.setLineWidth(1.2)
    pdf.roundRect(x, y, width, height, 12, fill=1, stroke=1)
    pdf.setFillColor(colors.HexColor(FAINT))
    pdf.setFont("Helvetica-Bold", 8.5)
    pdf.drawString(x + 18, y + height - 26, label)
    pdf.setFillColor(colors.HexColor(INK))
    size = 27 if len(value) > 7 else 30
    pdf.setFont("Helvetica-Bold", size)
    pdf.drawString(x + 18, y + 40, value)
    pdf.setFillColor(colors.HexColor(SLATE))
    pdf.setFont("Helvetica", 9)
    pdf.drawString(x + 18, y + 16, _truncate(hint, 36))


def _panel(pdf: Any, x: float, y: float, width: float, height: float, colors: Any) -> None:
    pdf.setFillColor(colors.white)
    pdf.setStrokeColor(colors.HexColor(BORDER))
    pdf.setLineWidth(1.2)
    pdf.roundRect(x, y, width, height, 12, fill=1, stroke=1)


def _grouped_hours(
    values: dict[str, float], *, max_items: int = 4, min_share: float = 0.1
) -> list[tuple[str, float]]:
    """Ordena por horas y agrupa lo poco significativo en «Otros»."""
    total = sum(values.values())
    ordered = sorted(values.items(), key=lambda entry: (-entry[1], entry[0]))
    if total <= 0:
        return ordered[:max_items]
    main = [(label, value) for label, value in ordered[:max_items] if value / total >= min_share]
    if not main:
        main = ordered[:1]
    others = sum(value for _, value in ordered[len(main) :])
    if others > 0:
        main.append(("Otros", others))
    return main


def _donut(
    pdf: Any,
    x: float,
    y: float,
    width: float,
    height: float,
    totals: dict[str, float],
    colors: Any,
) -> None:
    pdf.setFillColor(colors.HexColor(INK))
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(x + 22, y + height - 30, "Distribución del tiempo")
    total = sum(totals.values())
    center_x, center_y, radius, hole = x + 92, y + 76, 56, 32

    if total <= 0:
        pdf.setFont("Helvetica", 10)
        pdf.drawString(x + 22, y + 76, "Sin horas registradas en el periodo.")
        return

    angle = 90.0
    for label, value in totals.items():
        if value <= 0:
            continue
        extent = -360.0 * value / total
        pdf.setFillColor(colors.HexColor(TYPE_COLORS[label]))
        pdf.wedge(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            angle,
            extent,
            fill=1,
            stroke=0,
        )
        angle += extent
    pdf.setFillColor(colors.white)
    pdf.circle(center_x, center_y, hole, fill=1, stroke=0)
    pdf.setFillColor(colors.HexColor(INK))
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(center_x, center_y + 1, f"{_number(total)} h")
    pdf.setFillColor(colors.HexColor(SLATE))
    pdf.setFont("Helvetica", 8)
    pdf.drawCentredString(center_x, center_y - 12, "totales")

    legend_x = x + 186
    legend_y = y + 118
    for label, value in totals.items():
        share = round(100 * value / total)
        pdf.setFillColor(colors.HexColor(TYPE_COLORS[label]))
        pdf.roundRect(legend_x, legend_y - 2, 11, 11, 3, fill=1, stroke=0)
        pdf.setFillColor(colors.HexColor(INK))
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(legend_x + 19, legend_y, label)
        pdf.setFillColor(colors.HexColor(SLATE))
        pdf.setFont("Helvetica", 9)
        pdf.drawString(legend_x + 19, legend_y - 13, f"{_number(value)} h · {share}%")
        legend_y -= 34


def _hours_bars(
    pdf: Any,
    x: float,
    y: float,
    width: float,
    height: float,
    title: str,
    entries: list[tuple[str, float]],
    colors: Any,
    *,
    label_width: float = 125,
) -> None:
    pdf.setFillColor(colors.HexColor(INK))
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(x, y + height - 2, title)
    maximum = max((value for _, value in entries), default=1) or 1
    palette = (BLUE, CYAN, VIOLET, "#4C6FE0")
    bar_span = width - label_width - 42
    for index, (label, value) in enumerate(entries):
        row_y = y + height - 42 - index * 27
        color = GRAY if label == "Otros" else palette[index % len(palette)]
        pdf.setFillColor(colors.HexColor(INK))
        pdf.setFont("Helvetica", 9)
        pdf.drawString(x, row_y + 3, _truncate(label, int(label_width / 5.2)))
        pdf.setFillColor(colors.HexColor(TRACK))
        pdf.roundRect(x + label_width, row_y, bar_span, 12, 6, fill=1, stroke=0)
        pdf.setFillColor(colors.HexColor(color))
        pdf.roundRect(
            x + label_width,
            row_y,
            max(8, bar_span * value / maximum),
            12,
            6,
            fill=1,
            stroke=0,
        )
        pdf.setFillColor(colors.HexColor(INK))
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawRightString(x + width, row_y + 3, f"{_number(value)} h")
    if not entries:
        pdf.setFont("Helvetica", 10)
        pdf.drawString(x, y + 58, "Sin datos para el periodo.")


def _daily_chart(
    pdf: Any, x: float, y: float, width: float, height: float, values: dict[date, float], colors: Any
) -> None:
    pdf.setFillColor(colors.HexColor(INK))
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(x, y + height + 8, "Horas registradas por día")
    maximum = max(values.values(), default=0) or 1
    gap = 18
    bar_width = (width - gap * 6) / 7
    labels = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    baseline = y + 16
    pdf.setStrokeColor(colors.HexColor(BORDER))
    pdf.setLineWidth(1)
    pdf.line(x, baseline, x + width, baseline)
    for index, (day, hours) in enumerate(values.items()):
        bar_height = 56 * hours / maximum
        bar_x = x + index * (bar_width + gap)
        if hours:
            pdf.setFillColor(colors.HexColor(CYAN))
            radius = min(4.0, bar_height / 2)
            pdf.roundRect(bar_x, baseline, bar_width, bar_height, radius, fill=1, stroke=0)
        pdf.setFillColor(colors.HexColor(INK))
        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawCentredString(bar_x + bar_width / 2, baseline + bar_height + 6, _number(hours))
        pdf.setFillColor(colors.HexColor(SLATE))
        pdf.setFont("Helvetica", 8)
        pdf.drawCentredString(bar_x + bar_width / 2, y + 2, labels[index])


def _list_panel(
    pdf: Any,
    x: float,
    y: float,
    width: float,
    height: float,
    title: str,
    items: list[Activity],
    colors: Any,
    simple_split: Any,
    *,
    empty: str,
) -> None:
    _panel(pdf, x, y, width, height, colors)
    pdf.setFillColor(colors.HexColor(INK))
    pdf.setFont("Helvetica-Bold", 17)
    pdf.drawString(x + 22, y + height - 36, title)
    cursor = y + height - 73
    if not items:
        pdf.setFont("Helvetica", 11)
        pdf.drawString(x + 22, cursor, empty)
        return
    for item in items:
        pdf.setFillColor(colors.HexColor(TYPE_COLORS[work_type(item)]))
        pdf.circle(x + 28, cursor + 4, 4, fill=1, stroke=0)
        pdf.setFillColor(colors.HexColor(INK))
        pdf.setFont("Helvetica-Bold", 10)
        lines = simple_split(item.title, "Helvetica-Bold", 10, width - 68)[:2]
        for line in lines:
            pdf.drawString(x + 42, cursor, line)
            cursor -= 12
        pdf.setFillColor(colors.HexColor(SLATE))
        pdf.setFont("Helvetica", 8)
        meta = f"{item.category} · {item.status} · {_number(item.hours)} h"
        pdf.drawString(x + 42, cursor - 1, _truncate(meta, 58))
        cursor -= 32


def _table(pdf: Any, x: float, y: float, items: list[Activity], colors: Any, simple_split: Any) -> None:
    widths = [72, 368, 100, 108, 120, 57]
    headers = ["FECHA", "ACTIVIDAD", "TIPO", "MÓDULO", "ESTADO", "HORAS"]
    top = 402
    header_height = 26
    row_height = 30
    total_width = sum(widths)

    if not items:
        _panel(pdf, x, top - 78, total_width, 58, colors)
        pdf.setFillColor(colors.HexColor(SLATE))
        pdf.setFont("Helvetica", 12)
        pdf.drawString(x + 18, top - 53, "No hay actividades registradas en el periodo.")
        return

    bottom = top - len(items) * row_height
    pdf.setFillColor(colors.white)
    pdf.setStrokeColor(colors.HexColor(BORDER))
    pdf.setLineWidth(1.2)
    pdf.roundRect(
        x, bottom - 6, total_width, top + header_height - bottom + 6, 12, fill=1, stroke=1
    )
    pdf.setFillColor(colors.HexColor(ZEBRA))
    for row_index in range(1, len(items), 2):
        pdf.rect(
            x + 2, top - (row_index + 1) * row_height, total_width - 4, row_height, fill=1, stroke=0
        )

    cursor_x = x
    pdf.setFillColor(colors.HexColor(FAINT))
    pdf.setFont("Helvetica-Bold", 8)
    for header, width in zip(headers, widths):
        pdf.drawString(cursor_x + 8, top + 8, header)
        cursor_x += width
    pdf.setStrokeColor(colors.HexColor(BORDER))
    pdf.setLineWidth(1)
    pdf.line(x + 2, top, x + total_width - 2, top)

    for row_index, item in enumerate(items):
        row_y = top - (row_index + 1) * row_height
        columns = [
            (item.reported_on.strftime("%d/%m/%Y"), "Helvetica", SLATE),
            (item.title, "Helvetica-Bold", INK),
            (work_type(item), "Helvetica", SLATE),
            (item.module, "Helvetica", SLATE),
            (item.status, None, None),
            (_number(item.hours), "Helvetica-Bold", INK),
        ]
        cursor_x = x
        for column, ((value, font, color), width) in enumerate(zip(columns, widths)):
            if column == 4:
                _status_pill(pdf, cursor_x + 7, row_y + 8, str(value), colors)
            else:
                pdf.setFillColor(colors.HexColor(color))
                pdf.setFont(font, 8)
                lines = simple_split(str(value), font, 8, width - 14)[:2]
                if len(lines) == 1:
                    pdf.drawString(cursor_x + 7, row_y + 12, lines[0])
                else:
                    pdf.drawString(cursor_x + 7, row_y + 17, lines[0])
                    pdf.drawString(cursor_x + 7, row_y + 7, lines[1])
            cursor_x += width


def _status_pill(pdf: Any, x: float, y: float, status: str, colors: Any) -> None:
    background, foreground = STATUS_STYLES.get(_normalize(status), STATUS_DEFAULT)
    label = _truncate(status, 16)
    width = pdf.stringWidth(label, "Helvetica-Bold", 7.5) + 14
    pdf.setFillColor(colors.HexColor(background))
    pdf.roundRect(x, y, width, 15, 7.5, fill=1, stroke=0)
    pdf.setFillColor(colors.HexColor(foreground))
    pdf.setFont("Helvetica-Bold", 7.5)
    pdf.drawString(x + 7, y + 4.5, label)


def _footer(pdf: Any, start: date, end: date, page: int, colors: Any, period: str) -> None:
    pdf.setFillColor(colors.HexColor(FAINT))
    pdf.setFont("Helvetica", 8)
    prefix = "Semana" if period == "semanal" else "Día"
    pdf.drawString(48, 28, f"{prefix} {_range_label(start, end)}")
    pdf.drawRightString(912, 28, str(page))


def _value(properties: dict[str, Any], name: str) -> Any:
    return property_value(properties.get(name, {})) if name else ""


def _as_date(value: Any) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str) and value:
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
        except ValueError:
            return None
    return None


def _hours(value: Any) -> float:
    try:
        return max(float(value or 0), 0)
    except (TypeError, ValueError):
        return 0


def _text(value: Any) -> str:
    return str(value or "").strip()


def _normalize(value: str) -> str:
    return "".join(
        character
        for character in unicodedata.normalize("NFD", value.casefold())
        if unicodedata.category(character) != "Mn"
    )


def _is_done(status: str) -> bool:
    return _normalize(status) in DONE_STATUSES


def _number(value: float) -> str:
    return f"{value:.1f}".rstrip("0").rstrip(".")


def _range_label(start: date, end: date) -> str:
    months = (
        "enero",
        "febrero",
        "marzo",
        "abril",
        "mayo",
        "junio",
        "julio",
        "agosto",
        "septiembre",
        "octubre",
        "noviembre",
        "diciembre",
    )
    if start == end:
        return f"{start.day} de {months[start.month - 1]} de {start.year}"
    if start.month == end.month:
        return f"{start.day} al {end.day} de {months[end.month - 1]} de {end.year}"
    return (
        f"{start.day} de {months[start.month - 1]} al "
        f"{end.day} de {months[end.month - 1]} de {end.year}"
    )


def _truncate(value: str, length: int) -> str:
    return value if len(value) <= length else value[: length - 1].rstrip() + "…"


def _reportlab() -> tuple[Any, Any, Any]:
    try:
        from reportlab.lib import colors
        from reportlab.lib.utils import simpleSplit
        from reportlab.pdfgen import canvas
    except ImportError as exc:
        raise WeeklyReportError(
            "Falta reportlab. Instala el proyecto con: python3 -m pip install -e ."
        ) from exc
    return canvas, colors, simpleSplit
