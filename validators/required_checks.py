import streamlit as st
import pandas as pd

# Funktion zur Pflichtfeldprüfung, welche leere Felder wie NaN oder None durchsucht, aber auch leere Strings ("")
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
        st.error(f"Fehlende Werte bei Pflichtfeldern in **{filename}**:")
        for col, msg in missing_report.items():
            st.write(f"- **{col}**: {msg}")
    else:
        st.success(f"🎉 Alle Pflichtfelder in **{filename}** sind vollständig.")