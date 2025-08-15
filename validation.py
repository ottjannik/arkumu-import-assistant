# validation.py
# Diese Datei enthält die Validierungslogik für die verschiedenen CSV-Dateien

import streamlit as st
import pandas as pd

# Funktion zur Pflichtfeldprüfung, welche leere Felder wie NaN oder None durchsucht, aber auch leere Strings ("")
def check_required_columns_short(df, required_columns, filename):
    missing_report = {}
    for col in required_columns:
        if col not in df.columns:
            missing_report[col] = "Spalte fehlt"
        else:
            missing_count = df[col].isnull().sum() + (df[col] == "").sum()
            if missing_count > 0:
                missing_report[col] = f"{missing_count} fehlende(r) Wert(e)"
    if missing_report:
        st.error(f"Fehlende Werte bei Pflichtfeldern in **{filename}**")
    else:
        st.success(f"Alle Pflichtfelder in **{filename}** sind befüllt.")


def check_required_columns_detailed(df, required_columns, filename):
    missing_entries = []

    for col in required_columns:
        if col not in df.columns:
            missing_entries.append({"Projekt_ID": None, "Fehlende_Spalte": col, "Status": "Spalte fehlt"})
        else:
            missing_rows = df[df[col].isnull() | (df[col] == "")]
            for _, row in missing_rows.iterrows():
                missing_entries.append({
                    "Projekt_ID": row["Projekt_ID"],
                    "Fehlende_Spalte": col,
                    "Status": "Wert fehlt"
                })

    if missing_entries:
        st.error(f"Fehlende Werte bei Pflichtfeldern in **{filename}**")
        with st.expander("Details anzeigen", expanded=True):
            st.dataframe(pd.DataFrame(missing_entries))
    else:
        st.success(f"Alle Pflichtfelder in **{filename}** sind vollständig.")

def check_conditional_required_columns(df, conditional_rules, filename):
    """
    Prüft für jedes 'if_filled' Feld, ob bei Befüllung auch alle zugehörigen 'then_required' Felder vorhanden sind.

    Args:
        df (pd.DataFrame): Das zu prüfende DataFrame.
        conditional_rules (list): Liste von Regeln mit 'if_filled' und 'then_required' (Liste!).
        filename (str): Dateiname für Kontext im Reporting.

    Gibt bei Fehlern eine Streamlit-Warnung mit den betroffenen Zeilen aus.
    """
    for rule in conditional_rules:
        if_col = rule.get("if_filled")
        then_cols = rule.get("then_required", [])

        if if_col not in df.columns:
            st.warning(f"Spalte '{if_col}' fehlt in {filename}.")
            continue

        for then_col in then_cols:
            if then_col not in df.columns:
                st.warning(f"Spalte '{then_col}' fehlt in {filename}.")
                continue

            missing_rows = df[
                df[if_col].notna() & (df[if_col].astype(str).str.strip() != "") &
                (df[then_col].isna() | (df[then_col].astype(str).str.strip() == ""))
            ]

            if not missing_rows.empty:
                with st.expander(f"'{then_col}' fehlt, wenn '{if_col}' gesetzt ist ({filename}, {len(missing_rows)} Zeilen)"):
                    st.dataframe(missing_rows[[if_col, then_col]])