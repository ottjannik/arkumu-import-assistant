# =============================================================
# utils.py
# Diese Datei enthält Hilfsfunktionen, die in verschiedenen Teilen der Anwendung verwendet werden
# =============================================================

import streamlit as st
import time
# import pandas as pd

# ============================================================
# Funktionen zum Hochladen von Dateien
# ============================================================

def handle_file_upload(required_files):
    """Funktion zum Hochladen von Dateien über die Sidebar.
    Zeigt eine Erfolgsmeldung an, wenn Dateien hochgeladen werden,
    und überprüft, ob alle erforderlichen Dateien vorhanden sind.

    Args:
        required_files (list): Liste der erforderlichen Dateinamen.
    Returns:
        list: Liste der hochgeladenen Dateien oder None, wenn nicht alle erforderlichen Dateien vorhanden
    """
    files = st.sidebar.file_uploader(
        "CSV-Dateien:",
        accept_multiple_files=True,
        type='csv'
    )

    if files:
        if len(files) > st.session_state.get("uploaded_files_count", 0):
            new_files = len(files) - st.session_state.get("uploaded_files_count", 0)
            alert = st.sidebar.success(f"{new_files} Datei(en) erfolgreich hochgeladen!", icon="✅")
            st.session_state.uploaded_files_count = len(files)
            time.sleep(2)
            alert.empty()

        uploaded_names = [file.name for file in files]
        missing_files = set(required_files) - set(uploaded_names)
        if missing_files:
            st.sidebar.error(f"❗ Es fehlen {len(missing_files)} erforderliche Datei(en):")
            with st.sidebar.expander(f"Fehlende Datei(en):", expanded=True):
                for missing in sorted(missing_files):
                    st.markdown(f"{missing}")
            return None
        return files
    return None


# # Funktion zum Einlesen der CSV Dateien in Dataframes
# def read_csv_file(files, target_name, sep=";"):
#     for file in files:
#          if file.name == target_name:
#             try:
#                 return pd.read_csv(file, sep=sep)
#             except Exception as e:
#                 st.error(f"Fehler beim Lesen von '{file.name}': {e}")
#                 return None
#             return None

# # Funktion zum Laden aller DataFrames aus den hochgeladenen Dateien
# def load_all_dataframes(uploaded_files, required_files):
#     dfs = {}
#     for file_name in required_files:
#         df = read_csv_file(uploaded_files, file_name)
#         if df is not None:
#             dfs[file_name] = df
#     return dfs

# # Funktion zum Extrahieren von DataFrames mit spezifischen Namen
# def extract_named_dataframes(dfs):
#     return {
#         "projekte": dfs.get("00_Projekte.csv"),
#         "grundereignis": dfs.get("01_Grundereignis.csv"),
#         "akteurinnen": dfs.get("03_Personen_Akteurinnen.csv"),
#         "keywords": dfs.get("07_Kreuz_Projekte_Keywords.csv"),
#         "media": dfs.get("12_Media_DigitaleObjekte.csv"),
#     }