"""
Zentrales CSS-Styling für die Smart Weather App.
Alle visuellen Styles sind hier definiert und können zentral verwaltet werden.
"""
import streamlit as st


def load_app_styles():
    """
    Lädt alle CSS-Styles für die Anwendung.
    Wird einmalig am Anfang von app.py aufgerufen.
    """
    st.markdown("""
    <style>
        /* ===== METRIKEN & KARTEN ===== */
        .metric-card {
            padding: 16px;
            background: linear-gradient(135deg, #3b82f6 0%, #1e3a8a 100%);
            border-radius: 12px;
            color: white;
            text-align: center;
            box-shadow: 0 2px 8px rgba(30, 58, 138, 0.15);
        }
        
        .day-card {
            padding: 12px;
            border-radius: 10px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            border: 1px solid #d0d0d0;
        }
        
        .day-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
        }
        
        .day-selected {
            border: 2px solid #3b82f6;
            background: #eff6ff !important;
        }
        
        /* ===== WOCHENKARTEN ===== */
        .week-day-card {
            /* Inline-Styles werden durch Funktion gesetzt */
        }
        
        /* ===== BUTTONS ===== */
        div.stButton > button:first-child {
            height: 2.8rem;
            margin-top: 0.25rem;
        }
        
        /* ===== DARKMODE SUPPORT ===== */
        @media (prefers-color-scheme: dark) {
            .week-day-card {
                background: #111827 !important;
                color: #e5e7eb !important;
                border-color: #374151 !important;
            }
            
            .week-day-card small,
            .week-day-card div {
                color: #e5e7eb !important;
            }
        }
        
    </style>
    """, unsafe_allow_html=True)
