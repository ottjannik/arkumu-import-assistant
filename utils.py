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

# Funktion zur Pflichtfeldprüfung
def check_required_columns(df, required_columns, filename):
    missing_report = {}
    for col in required_columns:
        if col not in df.columns:
            missing_report[col] = "Spalte fehlt"
        else:
            missing_count = df[col].isnull().sum() + (df[col] == "").sum()
            if missing_count > 0:
                missing_report[col] = f"{missing_count} fehlende(r) Wert(e)"
    if missing_report:
        with st.expander(f"❗Fehlende Werte bei Pflichtfeldern in **{filename}**:", expanded=True):
            for col, msg in missing_report.items():
                st.write(f"- **{col}**: {msg}")
    else:
        st.success(f"🎉 Alle Pflichtfelder in **{filename}** sind vollständig.")