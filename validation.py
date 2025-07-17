# Validierungsfunktionen
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
        st.success(f"Alle Pflichtfelder in **{filename}** sind vollständig.")


def check_required_columns_detailed(df, required_columns, filename):
    missing_entries = []

    if "Projekt_ID" not in df.columns:
        st.error(f"Die Spalte 'Projekt_ID' fehlt in **{filename}** — Prüfung abgebrochen.")
        return

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

def check_conditional_required_columns(df, conditional_rules):
    report = {}

    for rule in conditional_rules:
        if_col = rule.get("if_filled")
        then_cols = rule.get("then_required", [])

        if if_col not in df.columns:
            report[if_col] = "Spalte fehlt für Bedingungsprüfung"
            continue

        for then_col in then_cols:
            if then_col not in df.columns:
                report[then_col] = "Spalte fehlt als Pflichtfeld"
                continue

            # Zeilen finden, bei denen Bedingung verletzt wird
            missing_rows = df[
                (df[if_col].notnull()) & (df[if_col] != "") &  # if_filled ist befüllt
                ((df[then_col].isnull()) | (df[then_col] == ""))  # then_required fehlt
            ]

            if not missing_rows.empty:
                report[f"{then_col} (wenn {if_col} gesetzt)"] = len(missing_rows)

    return report