# ============================================================
# app.py
# Diese Datei ist der Einstiegspunkt für die Streamlit-Anwendung
# Sie lädt die Konfigurationen, verarbeitet die hochgeladenen Dateien
# und zeigt die gerenderten Tabs der Anwendung an.
# ============================================================

import json
import streamlit as st

from utils import (
    handle_file_upload,
    load_all_dataframes,
    extract_named_dataframes,
)
from views import (
    render_overview_tab,
#     render_validation_tab,
#     render_projects_tab,
#     render_files_tab
)

# ============================================================
# 1. Seitenkonfiguration und Titel
# ============================================================

st.set_page_config(page_title='arkumu.nrw Import Assistant', page_icon='📁', layout="wide")
st.title('📁 arkumu.nrw Import Assistant')

# ============================================================
# 2. Sidebar
# ============================================================

    # ------------------------------------------------------------
    # 2.1 Profile laden, um Konfigurationen zu definieren
    # ------------------------------------------------------------

profiles = {
    "KHM": "configs/khm.json",
    "HfMT": "configs/hfmt.json"
}

st.sidebar.header("Metadaten-Upload")
st.sidebar.write("1. Wähle eine Datenquelle aus, um die entsprechenden Konfigurationen zu laden")
selected_profile = st.sidebar.selectbox("Datenquelle:", list(profiles.keys()))
profile_path = profiles[selected_profile]

with open(profile_path, "r", encoding="utf-8") as f:
    config = json.load(f)

required_files = config["required_files"]
required_columns = config["required_columns"]
conditional_required_columns = config.get("conditional_required_columns", {})
validation_targets = config["validation_targets"]

    # ------------------------------------------------------------
    # 2.2 Metadaten-Upload
    # ------------------------------------------------------------

st.sidebar.write("2. Lade die erforderlichen CSV-Dateien hoch")
uploaded_files = handle_file_upload(required_files, selected_profile)

if uploaded_files:
    dfs = load_all_dataframes(uploaded_files, required_files)
    named_dfs = extract_named_dataframes(dfs, validation_targets)

# ============================================================
# 3. Tabs und deren Inhalte
# ============================================================

    tabs = st.tabs(["Übersicht", "Projekte", "Dateien", "Pflichtfelder"])

    # ------------------------------------------------------------
    # 3.1 Übersichts-Tab (views.py / render_overview_tab)
    # ------------------------------------------------------------

    with tabs[0]:
        render_overview_tab(named_dfs, required_columns, conditional_required_columns)

    # ------------------------------------------------------------
    # 3.2 Projekte-Tab (views.py / render_projects_tab)
    # ------------------------------------------------------------

    # with tabs[1]:
    #     render_projects_tab(
    #         named_dfs["projekte"],
    #         named_dfs["akteurinnen"]
    #     )

    # with tabs[2]:
    #     render_files_tab(
    #         named_dfs["media"]
    #     )

    # with tabs[3]:
    #     render_validation_tab(
    #         dfs,
    #         required_columns,
    #         conditional_required_columns,
    #         validation_targets
    #     )

    # else:
    #     st.info("Diese Anwendung überprüft die hochgeladenen CSV-Dateien auf Vollständigkeit und Korrektheit.")
