import streamlit as st
import pandas as pd

# Page Infos
st.set_page_config(
    page_title="smart weather CH",
    page_icon="🌤️",
)

# Titel
st.title("Smart Weather CH")

# subtitle
st.subheader("Wilkommen zur Smart Weather CH Ihre persönliche Wetterquelle")

# columns
col1, col2 = st.columns(2)

with col1:
    location_input = st.text_input(placeholder = "Geben Sie Ihren eine Location ein")

with col2:
    querry_button = st.button("Suchen")
