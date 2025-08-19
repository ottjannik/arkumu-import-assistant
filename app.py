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
#    render_validation_tab,
#     render_projects_tab,
#     render_files_tab
)
from validation import validate_dataframe

# ============================================================
# 1. Seitenkonfiguration und Titel
# ============================================================

st.set_page_config(page_title='arkumu.nrw Import Assistant', page_icon='📁', layout="wide")
# st.logo("static/images/arkumu-logo-blue.svg", size="large", link=None, icon_image=None)
st.title('📁 arkumu.nrw Import Assistant')

# ============================================================
# 2. Sidebar
# ============================================================

# ------------------------------------------------------------
# 2.1 Profile laden, um Konfigurationen zu definieren
# ------------------------------------------------------------

profiles = {
    "KHM": "configs/khm.json",
    "HfMT (nicht verfügbar)": "configs/hfmt.json"
}

st.sidebar.header("📤 Metadaten-Upload")
st.sidebar.write("1. Wähle eine Datenquelle aus, um die entsprechenden Konfigurationen zu laden")

available_profiles = [p for p in profiles.keys() if "nicht verfügbar" not in p]

selected_profile = st.sidebar.selectbox(
    "Datenquelle:",
    options=profiles.keys(),
    index=0,
    help="HfMT wird angezeigt, ist aber aktuell nicht auswählbar"
)

if selected_profile not in available_profiles:
    st.warning("Dieses Profil ist aktuell nicht verfügbar. Bitte wähle ein anderes Profil.")
    st.stop()  # verhindert weiteres Ausführen
profile_path = profiles[selected_profile]

with open(profile_path, "r", encoding="utf-8") as f:
    config = json.load(f)

required_files = config["required_files"]
validation_targets = config["validation_targets"]
validation_targets_list = [
    {"df_key": key, "filename": val["filename"]}
    for key, val in validation_targets.items()
]
required_columns = {key: val.get("required", []) for key, val in validation_targets.items()}
conditional_required_columns = {key: val.get("conditional", []) for key, val in validation_targets.items()}
either_or_columns = {key: val.get("either_or", []) for key, val in validation_targets.items()}


# ------------------------------------------------------------
# 2.2 Metadaten-Upload
# ------------------------------------------------------------

st.sidebar.write("2. Lade die erforderlichen CSV-Dateien hoch")
uploaded_files = handle_file_upload(required_files, selected_profile)

if uploaded_files:
    dfs = load_all_dataframes(uploaded_files, required_files)
    named_dfs = extract_named_dataframes(dfs, validation_targets_list)

# ============================================================
# 3. Tabs und deren Inhalte
# ============================================================

    tabs = st.tabs(["Übersicht", "Projekte", "Dateien", "Pflichtfelder"])

# ------------------------------------------------------------
# 3.1 Übersichts-Tab (views.py / render_overview_tab)
# ------------------------------------------------------------

    with tabs[0]:
        render_overview_tab(named_dfs, validation_targets, required_columns, conditional_required_columns, either_or_columns)



# ------------------------------------------------------------
# 3.2 Validationsprüfung-Tab (views.py / )
# ------------------------------------------------------------

    with tabs[1]:
        validation_results = {}
        for df_key, df in named_dfs.items():
            rules = validation_targets[df_key]
            validation_results[df_key] = validate_dataframe(df, rules)

        for df_key, result in validation_results.items():
            filename = validation_targets[df_key]["filename"]

            overall_ok = all([
                result["required"]["ok"],
                result["conditional"]["ok"],
                result["either_or"]["ok"]
            ])
            status_icon = "✅" if overall_ok else "❌"

            with st.expander(f"{status_icon} {filename}"):
                if result["required"]["ok"]:
                    st.success("Alle Pflichtspalten erfüllt ✅")
                else:
                    st.error("Fehler bei Pflichtspalten ❌")
                    st.dataframe(result["required"]["errors"])

                if result["conditional"]["ok"]:
                    st.success("Alle Conditional-Regeln erfüllt ✅")
                else:
                    st.error("Fehler bei Conditional-Regeln ❌")
                    st.dataframe(result["conditional"]["errors"])

                if result["either_or"]["ok"]:
                    st.success("Alle Either/Or-Regeln erfüllt ✅")
                else:
                    st.error("Fehler bei Either/Or-Regeln ❌")
                    st.dataframe(result["either_or"]["errors"])




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
