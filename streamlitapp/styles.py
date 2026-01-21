"""
Zentrales CSS-Styling für die Smart Weather App.
Alle visuellen Styles sind hier definiert und können zentral verwaltet werden.

Darkmode-Unterstützung:
- System-Darkmode: @media (prefers-color-scheme: dark)
- Streamlit-Theme: body[data-theme="dark"] oder .theme-dark
"""
import streamlit as st


def load_app_styles():
    """
    Lädt alle CSS-Styles für die Anwendung.
    Wird einmalig am Anfang von app.py aufgerufen.
    Unterstützt sowohl System-Darkmode als auch Streamlit-Theme-Einstellungen.
    """
    st.markdown("""
    <style>
        /* ===== BASISSTYLES ===== */
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
        
        /* ===== WOCHENKARTEN BASISSTYLE ===== */
        .week-day-card {
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        /* ===== BUTTONS ===== */
        div.stButton > button:first-child {
            height: 2.8rem;
            margin-top: 0.25rem;
        }
        
        /* ===== DARKMODE: System (Handy, Desktop) ===== */
        @media (prefers-color-scheme: dark) {
            .week-day-card {
                background: #111827 !important;
                color: #000000 !important;
                border-color: #374151 !important;
            }
            
            .week-day-card * {
                color: #000000 !important;
            }
            
            .week-day-card small {
                color: #000000 !important;
            }
            
            .week-day-card div {
                color: #000000 !important;
            }
            
            .week-day-card strong {
                color: #000000 !important;
            }
            
            .day-card {
                background: #1f2937 !important;
                color: #000000 !important;
                border-color: #374151 !important;
            }
            
            .day-selected {
                border: 2px solid #ef4444 !important;
                background: #1f2937 !important;
            }
        }
        
        /* ===== DARKMODE: Streamlit-Theme (Variante A) ===== */
        /* Wenn Streamlit data-theme="dark" setzt */
        body[data-theme="dark"] .week-day-card {
            background: #111827 !important;
            color: #000000 !important;
            border-color: #374151 !important;
        }
        
        body[data-theme="dark"] .week-day-card * {
            color: #000000 !important;
        }
        
        body[data-theme="dark"] .week-day-card small {
            color: #000000 !important;
        }
        
        body[data-theme="dark"] .week-day-card div {
            color: #000000 !important;
        }
        
        body[data-theme="dark"] .week-day-card strong {
            color: #000000 !important;
        }
        
        body[data-theme="dark"] .day-card {
            background: #1f2937 !important;
            color: #000000 !important;
            border-color: #374151 !important;
        }
        
        body[data-theme="dark"] .day-selected {
            border: 2px solid #ef4444 !important;
            background: #1f2937 !important;
        }
        
        /* ===== DARKMODE: Streamlit-Theme (Variante B) ===== */
        /* Wenn Streamlit die Klasse theme-dark setzt */
        .theme-dark .week-day-card {
            background: #111827 !important;
            color: #000000 !important;
            border-color: #374151 !important;
        }
        
        .theme-dark .week-day-card * {
            color: #000000 !important;
        }
        
        .theme-dark .week-day-card small {
            color: #000000 !important;
        }
        
        .theme-dark .week-day-card div {
            color: #000000 !important;
        }
        
        .theme-dark .week-day-card strong {
            color: #000000 !important;
        }
        
        .theme-dark .day-card {
            background: #1f2937 !important;
            color: #000000 !important;
            border-color: #374151 !important;
        }
        
        .theme-dark .day-selected {
            border: 2px solid #ef4444 !important;
            background: #1f2937 !important;
        }
        
        /* ===== DARKMODE: Streamlit-Theme (Variante C) ===== */
        /* Wenn Streamlit data-testid mit dark setzt (häufig am PC) */
        [data-testid="stAppViewContainer"][data-theme="dark"] .week-day-card {
            background: #111827 !important;
            color: #000000 !important;
            border-color: #374151 !important;
        }
        
        [data-testid="stAppViewContainer"][data-theme="dark"] .week-day-card * {
            color: #000000 !important;
        }
        
        .stApp[data-theme="dark"] .week-day-card {
            background: #111827 !important;
            color: #000000 !important;
            border-color: #374151 !important;
        }
        
        .stApp[data-theme="dark"] .week-day-card * {
            color: #000000 !important;
        }
        
    </style>
    """, unsafe_allow_html=True)
