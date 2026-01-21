"""
Hilfsfunktionen und Konstanten für die Smart Weather App.
Deutsch-Formatierung, Datum-Manipulation, Woche-Berechnungen.
"""
import pandas as pd

# ===== DEUTSCHE TAGE UND MONATE =====
DEUTSCH_TAGE = {
    0: 'Montag', 1: 'Dienstag', 2: 'Mittwoch', 3: 'Donnerstag',
    4: 'Freitag', 5: 'Samstag', 6: 'Sonntag'
}

DEUTSCH_TAGE_KURZ = {
    0: 'Mo', 1: 'Di', 2: 'Mi', 3: 'Do',
    4: 'Fr', 5: 'Sa', 6: 'So'
}

DEUTSCH_MONATE = {
    1: 'Januar', 2: 'Februar', 3: 'März', 4: 'April',
    5: 'Mai', 6: 'Juni', 7: 'Juli', 8: 'August',
    9: 'September', 10: 'Oktober', 11: 'November', 12: 'Dezember'
}


# ===== DATUM-FORMATIERUNG =====
def format_date_german(date_obj, format_type='long'):
    """
    Formatiere Datum auf Deutsch.
    
    Args:
        date_obj: datetime.date oder datetime.datetime Objekt
        format_type: 'long' (Montag, 05.01.2026), 
                    'short' (Mo, 05.01), 
                    'long_full' (Montag, 05. Januar 2026)
    
    Returns:
        Formatierter Datum-String auf Deutsch
    """
    weekday = DEUTSCH_TAGE if format_type != 'short' else DEUTSCH_TAGE_KURZ
    day_name = weekday[date_obj.weekday()]
    
    if format_type == 'long':
        return f"{day_name}, {date_obj.strftime('%d.%m.%Y')}"
    elif format_type == 'short':
        return f"{day_name}\n{date_obj.strftime('%d.%m')}"
    elif format_type == 'long_full':
        month_name = DEUTSCH_MONATE[date_obj.month]
        return f"{day_name}, {date_obj.day}. {month_name} {date_obj.year}"
    return str(date_obj)


# ===== WOCHE & TAGE BERECHNUNGEN =====
def find_today_index(daily_df: pd.DataFrame) -> int:
    """
    Finde Index des heutigen Tages im daily_df.
    
    Args:
        daily_df: DataFrame mit 'date' Spalte
    
    Returns:
        Index des heutigen Tages oder 0 wenn nicht gefunden
    """
    today = pd.Timestamp.now().normalize()
    for idx, row in daily_df.iterrows():
        if pd.to_datetime(row["date"]).normalize() == today:
            return idx
    return 0


def get_week_start(offset_weeks: int = 0) -> pd.Timestamp:
    """
    Berechne Montag einer Woche mit optionalem Offset.
    
    Args:
        offset_weeks: Wochen-Offset (negativ = Vergangenheit, positiv = Zukunft)
    
    Returns:
        pd.Timestamp für Montag der Woche
    """
    today = pd.Timestamp.now().date()
    today_pd = pd.Timestamp(today)
    monday = today_pd - pd.Timedelta(days=today_pd.weekday())
    return monday + pd.Timedelta(days=offset_weeks * 7)


def slice_week(daily_df: pd.DataFrame, week_start: pd.Timestamp) -> pd.DataFrame:
    """
    Filtere daily_df für eine bestimmte Woche.
    
    Args:
        daily_df: DataFrame mit 'date' Spalte
        week_start: Montag der gewünschten Woche (pd.Timestamp)
    
    Returns:
        Gefilterte DataFrame für die Woche [week_start bis week_start+6 Tage]
    """
    week_end = week_start + pd.Timedelta(days=6)
    df = daily_df.copy()
    df["date"] = pd.to_datetime(df["date"]).dt.normalize()
    return df[(df["date"] >= week_start.normalize()) & (df["date"] <= week_end.normalize())]
