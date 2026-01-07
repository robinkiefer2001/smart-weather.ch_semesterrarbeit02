"""
Datenbankzugriff und SQL-Queries
"""
import streamlit as st
import pandas as pd
from typing import Optional, Tuple


def get_db_connection():
    """
    Gibt die Streamlit SQL-Verbindung zurück.
    """
    return st.connection("sql")


def search_location(search_term: str) -> Optional[Tuple[float, float]]:
    """
    Sucht einen Ort in der geo_location Tabelle.
    
    Args:
        search_term: Suchbegriff für den Ortsnamen
        
    Returns:
        Tuple mit (latitude, longitude) oder None wenn nicht gefunden
    """
    conn = get_db_connection()
    q = search_term.strip().replace("'", "''")
    
    result = conn.query(
        f"""
        SELECT latitude, longitude
        FROM geo_location
        WHERE name ILIKE '%{q}%'
        LIMIT 1;
        """
    )
    
    if len(result) == 0:
        return None
    
    return (float(result["latitude"][0]), float(result["longitude"][0]))
