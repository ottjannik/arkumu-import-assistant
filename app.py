# ============================================================
# app.py
# Diese Datei ist der Einstiegspunkt für die Streamlit-Anwendung
# Sie lädt die Konfigurationen, verarbeitet die hochgeladenen Dateien
# und rendert die verschiedenen Tabs der Anwendung.
# ============================================================

import time
import json
import streamlit as st

# from utils import (
#     load_all_dataframes,
#     extract_named_dataframes,
#     handle_file_upload
# )
# from views import (
#     render_overview_tab,
#     render_validation_tab,
#     render_projects_tab,
#     render_files_tab
# )

# ============================================================
# 1. Setup der Streamlit-Anwendung
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

def handle_file_upload(required_files):
    uploaded_files = st.sidebar.file_uploader(
        "CSV-Dateien:",
        accept_multiple_files=True,
        type='csv'
    )

    if uploaded_files:
        # Zähler aktualisieren und Erfolgsmeldung
        if len(uploaded_files) > st.session_state.get("uploaded_files_count", 0):
            new_files = len(uploaded_files) - st.session_state.get("uploaded_files_count", 0)
            alert = st.sidebar.success(f"{new_files} Datei(en) erfolgreich hochgeladen!", icon="✅")
            st.session_state.uploaded_files_count = len(uploaded_files)
            time.sleep(2)
            alert.empty()

        # Fehlende Dateien anzeigen
        uploaded_names = [file.name for file in uploaded_files]
        missing_files = set(required_files) - set(uploaded_names)
        if missing_files:
            with st.sidebar.expander(f"❗ Es fehlen {len(missing_files)} Datei(en):", expanded=True):
                for missing in sorted(missing_files):
                    st.markdown(f"- {missing}")
            return None  # unvollständig
        return uploaded_files
    return None




# uploaded_files = handle_file_upload(required_files)

if uploaded_files:
    pass
    # dfs = load_all_dataframes(uploaded_files, required_files)
    # named_dfs = extract_named_dataframes(dfs)

    # tabs = st.tabs(["Übersicht", "Projekte", "Dateien", "Pflichtfelder"])

    # with tabs[0]:
    #     render_overview_tab(
    #         named_dfs["projekte"],
    #         named_dfs["akteurinnen"],
    #         named_dfs["media"],
    #         named_dfs["grundereignis"],
    #         required_columns
    #     )

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

else:
    # st.session_state.uploaded_files_count = 0
    st.info("Bitte lade die benötigten CSV-Dateien hoch.")
    with st.sidebar.expander("📄 Benötigte CSV-Dateien", expanded=False):
        for file in sorted(required_files):
            st.markdown(f"{file}")