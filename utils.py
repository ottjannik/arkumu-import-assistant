# utils.py
# Diese Datei enthält Hilfsfunktionen, die in verschiedenen Teilen der Anwendung verwendet werden   

import pandas as pd
import streamlit as st
import time
from config import required_files

def handle_file_upload():
    uploaded_files = st.sidebar.file_uploader(
        "Choose CSV files to upload",
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


# Funktion zum Einlesen der CSV Dateien in Dataframes
def read_csv_file(files, target_name, sep=";"):
    for file in files:
         if file.name == target_name:
            try:
                return pd.read_csv(file, sep=sep)
            except Exception as e:
                st.error(f"Fehler beim Lesen von '{file.name}': {e}")
                return None
            return None
         
def load_all_dataframes(uploaded_files, required_files):
    dfs = {}
    for file_name in required_files:
        df = read_csv_file(uploaded_files, file_name)
        if df is not None:
            dfs[file_name] = df
    return dfs

def extract_named_dataframes(dfs):
    return {
        "projekte": dfs.get("00_Projekte.csv"),
        "grundereignis": dfs.get("01_Grundereignis.csv"),
        "akteurinnen": dfs.get("03_Personen_Akteurinnen.csv"),
        "keywords": dfs.get("07_Kreuz_Projekte_Keywords.csv"),
        "media": dfs.get("12_Media_DigitaleObjekte.csv"),
    }