# app.py
# Diese Datei ist der Einstiegspunkt für die Streamlit-Anwendung

import streamlit as st
import time
from config import required_files
from utils import (
    load_all_dataframes, 
    extract_named_dataframes, 
    handle_file_upload
)
from views import (
    render_overview_tab,
    render_validation_tab,
    render_projects_tab,
    render_files_tab
)

st.set_page_config(page_title='KHM → arkumu.nrw', page_icon='📁', layout="wide")
st.title('📁 KHM → arkumu.nrw')

# Upload und Prüfung
uploaded_files = handle_file_upload()

if uploaded_files:
    dfs = load_all_dataframes(uploaded_files, required_files)
    named_dfs = extract_named_dataframes(dfs)

    tabs = st.tabs(["Übersicht", "Projekte", "Dateien", "Pflichtfelder"])

    with tabs[0]:
        render_overview_tab(
            named_dfs["projekte"],
            named_dfs["akteurinnen"],
            named_dfs["media"],
            named_dfs["grundereignis"]
        )

    with tabs[1]:
        render_projects_tab(
            named_dfs["projekte"],
            named_dfs["akteurinnen"]
        )

    with tabs[2]:
        render_files_tab(
            named_dfs["media"]
        )

    with tabs[3]:
        render_validation_tab(dfs)

else:
    st.session_state.uploaded_files_count = 0
    st.info("Bitte lade die benötigten CSV-Dateien hoch.")
    with st.sidebar.expander("📄 Benötigte CSV-Dateien", expanded=False):
        for file in sorted(required_files):
            st.markdown(f"- {file}")