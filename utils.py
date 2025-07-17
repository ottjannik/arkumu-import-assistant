import pandas as pd
import streamlit as st

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

