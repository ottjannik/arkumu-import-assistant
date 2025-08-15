# utils.py
# Diese Datei enthält Hilfsfunktionen, die in verschiedenen Teilen der Anwendung verwendet werden   

import pandas as pd
import streamlit as st
import time



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

# Funktion zum Laden aller DataFrames aus den hochgeladenen Dateien
def load_all_dataframes(uploaded_files, required_files):
    dfs = {}
    for file_name in required_files:
        df = read_csv_file(uploaded_files, file_name)
        if df is not None:
            dfs[file_name] = df
    return dfs

# Funktion zum Extrahieren von DataFrames mit spezifischen Namen
def extract_named_dataframes(dfs):
    return {
        "projekte": dfs.get("00_Projekte.csv"),
        "grundereignis": dfs.get("01_Grundereignis.csv"),
        "akteurinnen": dfs.get("03_Personen_Akteurinnen.csv"),
        "keywords": dfs.get("07_Kreuz_Projekte_Keywords.csv"),
        "media": dfs.get("12_Media_DigitaleObjekte.csv"),
    }